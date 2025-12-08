#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_client.py
Descripción: Tests para HTTPClient base

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.api.client import HTTPClient, HTTPError


class TestHTTPClient:
    """Tests para HTTPClient"""

    def test_client_initialization(self):
        """Test inicialización del cliente"""
        client = HTTPClient(
            host="api.example.com",
            headers={"Authorization": "Bearer token"},
            timeout=60
        )

        assert client.host == "api.example.com"
        assert client.headers["Authorization"] == "Bearer token"
        assert client.timeout == 60

    def test_client_initialization_default_headers(self):
        """Test inicialización sin headers"""
        client = HTTPClient(host="api.example.com")

        assert client.host == "api.example.com"
        assert client.headers == {}
        assert client.timeout == 30  # Default

    @patch('http.client.HTTPSConnection')
    def test_get_request_success(self, mock_conn_class):
        """Test GET request exitoso"""
        # Mock de la respuesta
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"result": "success", "data": []}'

        # Mock de la conexión
        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.get("/test", {"param": "value"})

        assert result["result"] == "success"
        assert result["data"] == []
        mock_conn.request.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_get_request_with_params(self, mock_conn_class):
        """Test GET request con parámetros"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.get("/search", {"query": "test", "page": "1"})

        # Verificar que se llamó con los parámetros correctos
        call_args = mock_conn.request.call_args
        assert "/search?query=test&page=1" in call_args[0][1]

    @patch('http.client.HTTPSConnection')
    def test_get_request_without_params(self, mock_conn_class):
        """Test GET request sin parámetros"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.get("/endpoint")

        call_args = mock_conn.request.call_args
        assert call_args[0][1] == "/endpoint"

    @patch('http.client.HTTPSConnection')
    def test_get_request_http_error(self, mock_conn_class):
        """Test GET request con error HTTP"""
        mock_response = Mock()
        mock_response.status = 404
        mock_response.read.return_value = b'Not Found'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")

        with pytest.raises(HTTPError) as exc_info:
            client.get("/notfound")

        assert exc_info.value.status_code == 404
        assert "Not Found" in str(exc_info.value)
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_get_request_json_decode_error(self, mock_conn_class):
        """Test GET request con error de JSON"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'Invalid JSON{{'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")

        with pytest.raises(json.JSONDecodeError):
            client.get("/test")

        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_post_request_success(self, mock_conn_class):
        """Test POST request exitoso"""
        mock_response = Mock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"id": "123", "created": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.post("/create", {"name": "test"})

        assert result["id"] == "123"
        assert result["created"] is True
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_post_request_with_params_and_data(self, mock_conn_class):
        """Test POST request con parámetros y datos"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.post("/create", {"name": "test"}, {"api_version": "v1"})

        # Verificar parámetros en URL
        call_args = mock_conn.request.call_args
        assert "api_version=v1" in call_args[0][1]

        # Verificar body
        body = call_args[1]["body"]
        body_data = json.loads(body.decode('utf-8'))
        assert body_data["name"] == "test"

    @patch('http.client.HTTPSConnection')
    def test_post_request_status_200(self, mock_conn_class):
        """Test POST request con status 200"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.post("/update", {"id": "1"})

        assert result["ok"] is True

    @patch('http.client.HTTPSConnection')
    def test_post_request_http_error(self, mock_conn_class):
        """Test POST request con error HTTP"""
        mock_response = Mock()
        mock_response.status = 400
        mock_response.read.return_value = b'Bad Request'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")

        with pytest.raises(HTTPError) as exc_info:
            client.post("/create", {"invalid": "data"})

        assert exc_info.value.status_code == 400
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_post_request_sets_content_type(self, mock_conn_class):
        """Test POST request configura Content-Type"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com", headers={"X-Custom": "value"})
        result = client.post("/create", {"data": "test"})

        # Verificar headers
        call_args = mock_conn.request.call_args
        headers = call_args[1]["headers"]
        assert headers["Content-Type"] == "application/json"
        assert "Content-Length" in headers
        assert headers["X-Custom"] == "value"  # Header original preservado

    @patch('http.client.HTTPSConnection')
    def test_post_empty_data(self, mock_conn_class):
        """Test POST request sin datos"""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"ok": true}'

        mock_conn = Mock()
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        client = HTTPClient(host="api.example.com")
        result = client.post("/endpoint")

        # Verificar que se envió un objeto vacío
        call_args = mock_conn.request.call_args
        body = call_args[1]["body"]
        body_data = json.loads(body.decode('utf-8'))
        assert body_data == {}


class TestHTTPError:
    """Tests para HTTPError"""

    def test_http_error_creation(self):
        """Test creación de HTTPError"""
        error = HTTPError(404, "Not Found")

        assert error.status_code == 404
        assert error.message == "Not Found"
        assert "404" in str(error)
        assert "Not Found" in str(error)

    def test_http_error_without_message(self):
        """Test HTTPError sin mensaje"""
        error = HTTPError(500)

        assert error.status_code == 500
        assert error.message == ""
        assert "500" in str(error)
