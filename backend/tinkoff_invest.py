from datetime import datetime, date, timedelta
from tinkoff.invest import Client, RequestError, InstrumentIdType, CandleInterval
from tinkoff.invest.utils import quotation_to_float

def get_asset_price_by_date(asset_ticker: str, target_date: date, token: str) -> float | None:
    try:
        with Client(token) as client:
            # 1. Find the instrument by ticker to get its FIGI
            instruments_response = client.instruments.find_instrument(query=asset_ticker)
            
            if not instruments_response.instruments:
                print(f"Asset with ticker {asset_ticker} not found.")
                return None
            
            # Assuming the first result is the most relevant one
            instrument = instruments_response.instruments[0]
            figi = instrument.figi

            # 2. Get historical candle data for the target date
            # We request a range of one day (from target_date to target_date + 1 day)
            # to ensure we capture the candle for the target_date.
            from_date = datetime(target_date.year, target_date.month, target_date.day, tzinfo=target_date.tzinfo) # Removed .isoformat()
            to_date = from_date + timedelta(days=1)

            candles_response = client.market_data.get_candles(
                figi=figi,
                from_=from_date,
                to=to_date,
                interval=CandleInterval.CANDLE_INTERVAL_DAY
            )

            if not candles_response.candles:
                print(f"No historical data found for {asset_ticker} on {target_date}.")
                return None
            
            # 3. Extract the closing price for the target date
            # The API returns candles for the specified interval. For a daily interval,
            # we expect one candle for the target date if data exists.
            for candle in candles_response.candles:
                # Check if the candle's date matches the target date.
                # The candle.time is a datetime object, so compare its date part.
                if candle.time.date() == target_date:
                    return quotation_to_float(candle.close)
            
            print(f"No candle data specifically matching {target_date} found for {asset_ticker}.")
            return None

    except RequestError as e:
        print(f"Tinkoff Invest API error: {e.code.value} - {e.details}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
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
