import pytest
from fastapi.testclient import TestClient
from fastapi import status
from apps.users.infrastructure.controllers.user_controller import router 
