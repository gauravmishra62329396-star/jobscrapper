#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_rate_limiter.py
Descripción: Tests para RateLimiter

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
import time
from unittest.mock import Mock, patch
from src.api.rate_limiter import RateLimiter, retry_on_http_error


class TestRateLimiter:
    """Tests para RateLimiter"""

    def test_rate_limiter_initialization(self):
        """Test inicialización del rate limiter"""
        limiter = RateLimiter(delay=2.0, max_retries=5, retry_delay=3)

        assert limiter.delay == 2.0
        assert limiter.max_retries == 5
        assert limiter.retry_delay == 3
        assert limiter.request_count == 0
        assert limiter.last_request_time == 0.0

    def test_rate_limiter_default_values(self):
        """Test valores por defecto"""
        limiter = RateLimiter()

        assert limiter.delay == 1.0
        assert limiter.max_retries == 3
        assert limiter.retry_delay == 2

    @patch('time.sleep')
    @patch('time.time')
    def test_wait_first_request(self, mock_time, mock_sleep):
        """Test wait en primer request"""
        mock_time.return_value = 100.0

        limiter = RateLimiter(delay=1.0)
        limiter.wait()

        # No debería dormir en el primer request
        mock_sleep.assert_not_called()
        assert limiter.request_count == 1
        assert limiter.last_request_time == 100.0

    @patch('time.sleep')
    @patch('time.time')
    def test_wait_needs_delay(self, mock_time, mock_sleep):
        """Test wait cuando necesita delay"""
        # Simular dos requests muy rápidos
        # wait() llama a time.time() 2 veces: al inicio y al final
        # Primer wait(): 100.0 (inicio), 100.0 (final)
        # Segundo wait(): 100.5 (inicio), 100.5 (final)
        mock_time.side_effect = [100.0, 100.0, 100.5, 100.5]

        limiter = RateLimiter(delay=1.0)
        limiter.wait()  # Primer request
        limiter.wait()  # Segundo request

        # Debería dormir 0.5 segundos (1.0 - 0.5)
        mock_sleep.assert_called_once()
        sleep_time = mock_sleep.call_args[0][0]
        assert 0.4 < sleep_time < 0.6  # Aproximadamente 0.5

    @patch('time.sleep')
    @patch('time.time')
    def test_wait_no_delay_needed(self, mock_time, mock_sleep):
        """Test wait cuando no necesita delay"""
        # Simular que pasó suficiente tiempo
        # Primer wait(): 100.0 (inicio), 100.0 (final)
        # Segundo wait(): 102.0 (inicio), 102.0 (final)
        mock_time.side_effect = [100.0, 100.0, 102.0, 102.0]

        limiter = RateLimiter(delay=1.0)
        limiter.wait()  # Primer request
        limiter.wait()  # Segundo request

        # No debería dormir porque pasó más del delay
        assert mock_sleep.call_count == 0

    def test_with_retry_success_first_attempt(self):
        """Test with_retry con éxito en primer intento"""
        limiter = RateLimiter(delay=0.01)  # Delay pequeño para tests

        @limiter.with_retry
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"
        assert limiter.request_count == 1

    @patch('time.sleep')
    def test_with_retry_success_after_retries(self, mock_sleep):
        """Test with_retry con éxito después de reintentos"""
        limiter = RateLimiter(delay=0.01, max_retries=3, retry_delay=1)
        attempt_count = [0]

        @limiter.with_retry
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise Exception("Temporary error")
            return "success"

        result = test_func()
        assert result == "success"
        assert attempt_count[0] == 3
        assert limiter.request_count == 3

    @patch('time.sleep')
    def test_with_retry_all_attempts_fail(self, mock_sleep):
        """Test with_retry cuando todos los intentos fallan"""
        limiter = RateLimiter(delay=0.01, max_retries=3, retry_delay=1)

        @limiter.with_retry
        def test_func():
            raise ValueError("Permanent error")

        with pytest.raises(ValueError) as exc_info:
            test_func()

        assert "Permanent error" in str(exc_info.value)
        assert limiter.request_count == 3  # Intentó 3 veces

    @patch('time.sleep')
    def test_with_retry_exponential_backoff(self, mock_sleep):
        """Test with_retry usa exponential backoff"""
        limiter = RateLimiter(delay=0.01, max_retries=3, retry_delay=2)
        attempt_count = [0]

        @limiter.with_retry
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 4:
                raise Exception("Error")
            return "success"

        with pytest.raises(Exception):
            test_func()

        # Verificar backoff: 2, 4, no sleep en último intento
        sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
        # Filtrar los sleeps de rate limiting (muy pequeños)
        backoff_sleeps = [s for s in sleep_calls if s > 0.1]
        assert len(backoff_sleeps) == 2  # Solo 2 backoffs (entre 3 intentos)
        assert backoff_sleeps[0] == 2  # Primer backoff
        assert backoff_sleeps[1] == 4  # Segundo backoff (exponencial)

    def test_with_retry_preserves_function_metadata(self):
        """Test with_retry preserva metadata de función"""
        limiter = RateLimiter(delay=0.01)

        @limiter.with_retry
        def test_func():
            """This is a test function"""
            return "test"

        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "This is a test function"

    def test_with_retry_with_args_and_kwargs(self):
        """Test with_retry con argumentos"""
        limiter = RateLimiter(delay=0.01)

        @limiter.with_retry
        def test_func(a, b, c=None):
            return f"{a}-{b}-{c}"

        result = test_func("x", "y", c="z")
        assert result == "x-y-z"


class TestRetryOnHttpError:
    """Tests para retry_on_http_error decorator"""

    @patch('time.sleep')
    def test_retry_on_http_error_success(self, mock_sleep):
        """Test decorator con éxito inmediato"""
        @retry_on_http_error(max_retries=3, retry_delay=1)
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    def test_retry_on_http_error_429_retries(self, mock_sleep):
        """Test decorator reintenta en error 429"""
        attempt_count = [0]

        @retry_on_http_error(max_retries=3, retry_delay=1)
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise Exception("HTTP 429 Rate limit")
            return "success"

        result = test_func()
        assert result == "success"
        assert attempt_count[0] == 3

    @patch('time.sleep')
    def test_retry_on_http_error_timeout_retries(self, mock_sleep):
        """Test decorator reintenta en timeout"""
        attempt_count = [0]

        @retry_on_http_error(max_retries=2, retry_delay=1)
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise Exception("Connection timeout")
            return "success"

        result = test_func()
        assert result == "success"

    @patch('time.sleep')
    def test_retry_on_http_error_non_retryable(self, mock_sleep):
        """Test decorator no reintenta errores no retryables"""
        @retry_on_http_error(max_retries=3, retry_delay=1)
        def test_func():
            raise ValueError("HTTP 400 Bad Request")

        with pytest.raises(ValueError):
            test_func()

        # No debería haber dormido porque no es retryable
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    def test_retry_on_http_error_max_retries_reached(self, mock_sleep):
        """Test decorator alcanza máximo de reintentos"""
        @retry_on_http_error(max_retries=3, retry_delay=1)
        def test_func():
            raise Exception("429 rate limit")

        with pytest.raises(Exception) as exc_info:
            test_func()

        assert "429" in str(exc_info.value)
        # Debería haber dormido 2 veces (entre 3 intentos: intento1->sleep->intento2->sleep->intento3)
        assert mock_sleep.call_count == 2

    @patch('time.sleep')
    def test_retry_on_http_error_incremental_delay(self, mock_sleep):
        """Test decorator usa delay incremental"""
        attempt_count = [0]

        @retry_on_http_error(max_retries=3, retry_delay=2)
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 4:
                raise Exception("Connection error")
            return "success"

        with pytest.raises(Exception):
            test_func()

        # Verificar delays: 2, 4 (solo 2 sleeps entre 3 intentos)
        sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
        assert sleep_calls == [2, 4]

    def test_retry_on_http_error_preserves_metadata(self):
        """Test decorator preserva metadata"""
        @retry_on_http_error()
        def test_func():
            """Test function"""
            return "test"

        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Test function"

    @patch('time.sleep')
    def test_retry_on_http_error_with_args(self, mock_sleep):
        """Test decorator con argumentos"""
        @retry_on_http_error(max_retries=2)
        def test_func(x, y):
            return x + y

        result = test_func(5, 3)
        assert result == 8

    @patch('time.sleep')
    def test_retry_on_http_error_connection_error(self, mock_sleep):
        """Test decorator reintenta en connection error"""
        attempt_count = [0]

        @retry_on_http_error(max_retries=2, retry_delay=1)
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise Exception("Connection refused")
            return "success"

        result = test_func()
        assert result == "success"

    @patch('time.sleep')
    def test_retry_on_http_error_temporary_error(self, mock_sleep):
        """Test decorator reintenta en temporary error"""
        attempt_count = [0]

        @retry_on_http_error(max_retries=2, retry_delay=1)
        def test_func():
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise Exception("Temporary failure")
            return "success"

        result = test_func()
        assert result == "success"


    def test_retry_on_http_error_zero_retries(self):
        """Test decorator con max_retries=0 alcanza línea de código muerto"""
        @retry_on_http_error(max_retries=0, retry_delay=1)
        def test_func():
            return "success"

        # Con max_retries=0, el range(0) no itera, llega directo al raise final
        with pytest.raises(Exception) as exc_info:
            test_func()
        assert "Máximo de reintentos alcanzado" in str(exc_info.value)
