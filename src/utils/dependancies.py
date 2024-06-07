import pandas as pd
import numpy as np
import cv2
import hashlib
import psycopg2
import secrets
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
import smtplib
from email.mime.text import MIMEText
import os
import matplotlib.pyplot as plt
import mplcursors
import matplotlib
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from ultralytics import YOLO
