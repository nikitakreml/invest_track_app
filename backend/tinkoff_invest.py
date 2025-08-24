from datetime import datetime, date, timedelta, timezone
from tinkoff.invest import Client, RequestError, InstrumentIdType, CandleInterval
from . import crud, schemas

def quotation_to_float(quotation) -> float:
    return quotation.units + quotation.nano / 1_000_000_000

def get_asset_price_by_date(asset_ticker: str, target_date: date, token: str) -> float | None:
    print(f"Current server date: {date.today()}")
    print(f"Target date type: {type(target_date)}, value: {target_date}")

    if target_date > date.today():
        print(f"Cannot retrieve historical data for a future date: {target_date}.")
        return None

    try:
        with Client(token) as client:
            # 1. Find the instrument by ticker to get its FIGI
            instruments_response = client.instruments.find_instrument(query=asset_ticker)
            
            if not instruments_response.instruments:
                print(f"Asset with ticker {asset_ticker} not found.")
                return None
            
            # Prioritize shares with api_trade_available_flag=True
            instrument = None
            for inst in instruments_response.instruments:
                if inst.instrument_type == 'share' and inst.api_trade_available_flag:
                    instrument = inst
                    print(f"Selected primary SHARE instrument for {asset_ticker}: {instrument.figi} (Class: {instrument.class_code})")
                    break
            
            # If no share found, look for any instrument with api_trade_available_flag=True
            if instrument is None:
                for inst in instruments_response.instruments:
                    if inst.api_trade_available_flag:
                        instrument = inst
                        print(f"Selected API tradable NON-SHARE instrument for {asset_ticker}: {instrument.figi} (Type: {instrument.instrument_type}, Class: {instrument.class_code})")
                        break

            if instrument is None:
                # Fallback to the very first instrument if no API tradable instrument is found
                instrument = instruments_response.instruments[0]
                print(f"Warning: No API tradable instrument found for {asset_ticker}. Using the first available instrument: {instrument.figi} (Type: {instrument.instrument_type}, Class: {instrument.class_code})")

            figi = instrument.figi
            print(f"Found FIGI for {asset_ticker}: {figi}")
            print(f"Full Instrument Response for {asset_ticker}: {instruments_response}")
            print(f"Selected Instrument Details for {asset_ticker}:")
            print(f"  FIGI: {instrument.figi}")
            print(f"  Ticker: {instrument.ticker}")
            print(f"  Name: {instrument.name}")
            print(f"  Instrument Type: {instrument.instrument_type}")
            print(f"  Class Code: {instrument.class_code}")
            print(f"  API Trade Available: {instrument.api_trade_available_flag}")
            print(f"  First 1-Day Candle Date: {instrument.first_1day_candle_date.date() if instrument.first_1day_candle_date else 'N/A'}")

            # Check if historical data is available for the target date range
            if instrument.api_trade_available_flag is False:
                print(f"API trading not available for {asset_ticker}. This prevents fetching market data. Please ensure you are using an instrument that is available for API trading with your token.")
                return None

            # Tinkoff Invest API documentation states daily candles are available for up to one year.
            # Check the first available daily candle date.
            if instrument.first_1day_candle_date and target_date < instrument.first_1day_candle_date.date():
                print(f"Requested date {target_date} is before first available daily candle date {instrument.first_1day_candle_date.date()} for {asset_ticker}.")
                return None

            # 2. Handle current day price vs. historical daily candle
            if target_date == date.today():
                print(f"Target date is today. Attempting to get last price for {asset_ticker}.")
                last_prices_response = client.market_data.get_last_prices(figi=[figi])
                if last_prices_response.last_prices:
                    last_price = last_prices_response.last_prices[0]
                    price = quotation_to_float(last_price.price)
                    print(f"Retrieved last price for {asset_ticker} today: {price}")
                    return price
                else:
                    print(f"No last price found for {asset_ticker} today. Proceeding to check for daily candle (if trading day just ended).")
            
            # For historical dates, or if today's last price wasn't found, try daily candle
            # Define a wider range around the target day in UTC to catch potential edge cases
            start_of_range_utc = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc) - timedelta(days=5)
            end_of_range_utc = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc) + timedelta(days=5)
            
            print(f"Requesting daily candles for FIGI: {figi}, from: {start_of_range_utc}, to: {end_of_range_utc}")

            candles_response = client.market_data.get_candles(
                figi=figi,
                from_=start_of_range_utc,
                to=end_of_range_utc,
                interval=CandleInterval.CANDLE_INTERVAL_DAY
            )

            if not candles_response.candles:
                print(f"No historical daily candle data found for {asset_ticker} in the exact range {target_date}.")
                return None
            
            print(f"Candles received: {candles_response.candles}")

            # 3. Extract the closing price for the target date
            for candle in candles_response.candles:
                print(f"Processing candle: Time={candle.time}, Close={quotation_to_float(candle.close)}")
                # candle.time is already a timezone-aware datetime object
                if candle.time.date() == target_date:
                    print(f"Found daily candle for target date: {candle.time.date()}")
                    return quotation_to_float(candle.close)
            
            print(f"No daily candle data specifically matching {target_date} found for {asset_ticker} after filtering.")
            return None

    except RequestError as e:
        print(f"Tinkoff Invest API error: {e.code.value} - {e.details}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_current_asset_price(asset_ticker: str, token: str) -> float | None:
    """Fetches the current market price of an asset."""
    try:
        with Client(token) as client:
            instruments_response = client.instruments.find_instrument(query=asset_ticker)

            if not instruments_response.instruments:
                print(f"Asset with ticker {asset_ticker} not found.")
                return None

            # Prioritize shares with api_trade_available_flag=True
            instrument = None
            for inst in instruments_response.instruments:
                if inst.instrument_type == 'share' and inst.api_trade_available_flag:
                    instrument = inst
                    break
            
            # If no share found, look for any instrument with api_trade_available_flag=True
            if instrument is None:
                for inst in instruments_response.instruments:
                    if inst.api_trade_available_flag:
                        instrument = inst
                        break

            if instrument is None:
                print(f"Warning: No API tradable instrument found for {asset_ticker}. Cannot get current price. Token: {token}")
                return None

            figi = instrument.figi
            last_prices_response = client.market_data.get_last_prices(figi=[figi])

            if last_prices_response.last_prices:
                last_price = last_prices_response.last_prices[0]
                price = quotation_to_float(last_price.price)
                print(f"Retrieved current price for {asset_ticker}: {price}")
                return price
            else:
                print(f"No current price found for {asset_ticker}.")
                return None

    except RequestError as e:
        print(f"Tinkoff Invest API error: {e.code.value} - {e.details}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching current price: {e}")
        return None

# Example Usage (for testing purposes, remove in production)
# if __name__ == "__main__":
#     # Replace with your actual Tinkoff Invest API token and asset ticker
#     TINKOFF_API_TOKEN = "t.xxxxxx"
#     ASSET_TICKER = "SBER"
#     TARGET_DATE = date(2023, 10, 26)

#     price = get_asset_price_by_date(ASSET_TICKER, TARGET_DATE, TINKOFF_API_TOKEN)
#     if price is not None:
#         print(f"The closing price of {ASSET_TICKER} on {TARGET_DATE} was: {price}")
#     else:
#         print(f"Could not retrieve price for {ASSET_TICKER} on {TARGET_DATE}.")
