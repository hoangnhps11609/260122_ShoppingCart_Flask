from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response

from flask_mysqldb import MySQL

import MySQLdb.cursors

import re

import jwt
from datetime import datetime, timedelta
from functools import wraps
from saleapp import app, db

mysql = MySQL(app)


