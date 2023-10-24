from datetime import timedelta, datetime, time, date
import requests
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import pandas as pd
import runScript2
import streamlit as st

# implied = pd.DataFrame(data=runScript2.df['Timestamp'], columns=[runScript2.df['Underlying APY'], runScript2.df['Implied APY']])


st.line_chart(runScript2.df[['Timestamp', 'Underlying APY']])
