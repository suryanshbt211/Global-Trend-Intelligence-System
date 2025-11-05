from pytrends.request import TrendReq
import pandas as pd
import time
from typing import List

class PyTrendsService:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.rate_limit_delay = 1
        
    def fetch_interest_over_time(self, keywords: List[str], timeframe: str = "today 12-m", geo: str = ""):
        try:
            self.pytrends.build_payload(kw_list=keywords, cat=0, timeframe=timeframe, geo=geo, gprop='')
            data = self.pytrends.interest_over_time()
            time.sleep(self.rate_limit_delay)
            
            if data.empty:
                return pd.DataFrame()
            if 'isPartial' in data.columns:
                data = data.drop(columns=['isPartial'])
            return data
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return pd.DataFrame()
    
    def get_related_queries(self, keyword: str):
        try:
            self.pytrends.build_payload(kw_list=[keyword], timeframe='today 12-m')
            related = self.pytrends.related_queries()
            time.sleep(self.rate_limit_delay)
            
            if keyword in related and related[keyword]['top'] is not None:
                return related[keyword]['top']['query'].tolist()[:20]
            return []
        except Exception as e:
            print(f"Error fetching related queries: {e}")
            return []
    
    def get_interest_by_region(self, keyword: str):
        try:
            self.pytrends.build_payload(kw_list=[keyword], timeframe='today 12-m')
            regional_data = self.pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
            time.sleep(self.rate_limit_delay)
            return regional_data.sort_values(by=keyword, ascending=False).head(50)
        except Exception as e:
            print(f"Error fetching regional data: {e}")
            return pd.DataFrame()
    
    def detect_emerging_trends(self, category: int = 0):
        try:
            trending = self.pytrends.trending_searches(pn='united_states')
            time.sleep(self.rate_limit_delay)
            if not trending.empty:
                return trending[0].tolist()[:10]
            return []
        except Exception as e:
            print(f"Error detecting emerging trends: {e}")
            return []
