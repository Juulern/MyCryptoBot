import time

import pytest
import os

from data.sources.binance import BinanceDataHandler
from data.tests.helpers.mocks.modules import *
from data.tests.helpers.mocks.models import *
from data.tests.helpers.sample_data import processed_historical_data
from shared.utils.exceptions import InvalidInput
from shared.utils.test_setup import get_fixtures
from database.model.models import ExchangeData, StructuredData

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestBinanceDataHandler:

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_binance_data_handler(
        self,
        fixture,
        mock_binance_handler_klines,
        mock_binance_client_init,
        mock_binance_client_ping,
        mock_binance_handler_websocket,
        mock_binance_websocket_start,
        mock_trigger_signal_successfully,
        trigger_signal_spy,
        exchange_data
    ):

        params_dict = dict(
            strategy=fixture["in"]["strategy"],
            params=fixture["in"]["params"],
            symbol=fixture["in"]["symbol"],
            candle_size=fixture["in"]["candle_size"],
        )

        binance_data_handler = BinanceDataHandler(**params_dict)
        binance_data_handler.start_data_ingestion()

        assert ExchangeData.objects.all().count() == fixture["out"]["expected_number_objs_exchange"]
        assert StructuredData.objects.all().count() == fixture["out"]["expected_number_objs_structured"]
        assert StructuredData.objects.first().open_time.date() == processed_historical_data[0]["open_time"].date()

        trigger_signal_spy.assert_called_with(
            params_dict["symbol"],
            params_dict["strategy"],
            params_dict["params"],
            params_dict["candle_size"],
            'binance'
        )

    @pytest.mark.parametrize(
        "input_value",
        [
            pytest.param(
                {
                    "strategy": "MovingAverage",
                    "params": {"ma": 30},
                    "symbol": "BTCUSDT",
                    "candle_size": "5m"
                },
                id="InvalidStrategyParams",
            ),
        ],
    )
    def test_exception(
        self,
        input_value,
        mock_binance_client_init,
        mock_binance_client_ping,
        mock_binance_handler_websocket,
        exchange_data
    ):

        with pytest.raises(Exception) as excinfo:
            binance_data_handler = BinanceDataHandler(**input_value)
            binance_data_handler.start_data_ingestion()
            binance_data_handler.stop_data_ingestion()

        assert excinfo.type == InvalidInput
