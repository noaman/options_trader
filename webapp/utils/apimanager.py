import json
import os
import pandas as pd
import numpy as np
# Create your views here.


class ApiManager():

    def getbuiltupDF(self):
        data_df = self.getHeatMapDF('','',True)
        df_price_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="current_change",ascending=False)
        df_price_longbuild["price_rank"]="LPR"+(df_price_longbuild.reset_index().index+1).astype(str)
       
        df_oi_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="oi_change",ascending=False)
        df_oi_longbuild["oi_rank"]="LOR"+(df_oi_longbuild.reset_index().index+1).astype(str)
       
       
        df_price_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="current_change",ascending=True)
        df_price_shortbuild["price_rank"]="SPR"+(df_price_shortbuild.reset_index().index+1).astype(str)
        data_df_oi_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="oi_change",ascending=False)
        data_df_oi_shortbuild["oi_rank"]="SOR"+(data_df_oi_shortbuild.reset_index().index+1).astype(str)

        #df_master=pd.concat([df_price_longbuild,df_oi_longbuild], axis=0, ignore_index=True,join='outer')
        df_master_long = pd.merge(df_oi_longbuild,df_price_longbuild)
        df_master_short = df_price_shortbuild.merge(data_df_oi_shortbuild, how='inner')
        df_master=pd.concat([df_master_long,df_master_short], axis=0, ignore_index=True)

        df_master.to_excel("Output/master_ranking.xlsx")
        
        return{"df_master":df_master.to_html()}
        #return{"df_price_longbuild":df_price_longbuild.to_html(),"df_oi_longbuild":df_oi_longbuild.to_html(),"df_price_shortbuild":df_price_shortbuild.to_html(),"data_df_oi_shortbuild":data_df_oi_shortbuild.to_html()}

    def getFilePath(self):
        if("E:" in os.getcwd()):
            #return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
            #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
            return "/optionstrader/webapp/utils/"
        else:
            return "/var/www/optionstrader/webapp/utils/"

    def getIndustryHeatMap(self):
        df= self.getHeatMapDF('','',True)
        data_industry=df.groupby(['Sector'], group_keys=False).apply(lambda grp: list(grp.value_counts().index)).to_dict()
        return {"data":data_industry}

    def getScreenerDF(self,scrip='',getDf=False):
        fpath= self.getFilePath()+"options_screener.json"
        optionsscreenerdata={}
        with open(fpath, 'r') as f:
            optionsscreenerdata = json.load(f)

        last_updated = optionsscreenerdata["last_updated"]    
        data_df = pd.DataFrame.from_dict(optionsscreenerdata["data"] )
        if(scrip != ''):
            data_df=data_df[data_df["name"]==scrip]

        data_df = data_df.sort_values(by=["type","strike"],ascending=True)   
        # if(industry==True):
        #     data_industry=(dict(data_df.groupby('Industry').apply(list)))
        #     data_to_send={"last_updated":last_updated,"data":data_industry}
        # else:
        data=data_df.to_dict("records") 
        if(getDf):
            return data_df
        else:    
            data_to_send={"last_updated":last_updated,"data":data_df.to_dict("records")}
        
        return data_to_send

    def getHeatMapDF(self,sort='',scrip='',getDf=False):
        screener_df=self.getScreenerDF('',True)

        fpath=self.getFilePath()+"optionsheatmap.json"

        with open(fpath, 'r') as f:
            optionsmapdata = json.load(f)

        last_updated = optionsmapdata["last_updated"]    
        data_df = pd.DataFrame.from_dict(optionsmapdata["data"] )
        #data_df['screener_count'] = data_df["code"].isin(screener_df["name"])
        data_df['screener_count']=data_df['code'].map(screener_df['name'].value_counts())

        # ###new code for rankin
        df_price_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="current_change",ascending=False)
        df_price_longbuild["price_rank"]="LPR"+(df_price_longbuild.reset_index().index+1).astype(str)
       
        df_oi_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="oi_change",ascending=False)
        df_oi_longbuild["oi_rank"]="LOR"+(df_oi_longbuild.reset_index().index+1).astype(str)
       
       
        df_price_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="current_change",ascending=True)
        df_price_shortbuild["price_rank"]="SPR"+(df_price_shortbuild.reset_index().index+1).astype(str)
        data_df_oi_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="oi_change",ascending=False)
        data_df_oi_shortbuild["oi_rank"]="SOR"+(data_df_oi_shortbuild.reset_index().index+1).astype(str)

        #df_master=pd.concat([df_price_longbuild,df_oi_longbuild], axis=0, ignore_index=True,join='outer')
        df_master_long = pd.merge(df_oi_longbuild,df_price_longbuild)
        df_master_short = df_price_shortbuild.merge(data_df_oi_shortbuild, how='inner')
        df_master=pd.concat([df_master_long,df_master_short], axis=0, ignore_index=True)
        data_df=df_master
        # ##new code for rankin
        if(sort != ''):
            if(sort=='oi_change'):
                data_df = data_df.sort_values(by=sort,ascending=False)
            elif(sort=="price_longbuild"):
                data_df = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="current_change",ascending=False)
            elif(sort=="oi_longbuild"):
                data_df = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="oi_change",ascending=False)
            elif(sort=="price_shortbuild"):
                data_df = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="current_change",ascending=True)
            elif(sort=="oi_shortbuild"):
                data_df = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="oi_change",ascending=False)

            else:
                data_df = data_df.sort_values(by=sort,ascending=True)    

        if(scrip!=''):
            data_df=data_df[data_df["code"]==scrip]
        if(getDf):
            return data_df
        else:
            data_to_send={"last_updated":last_updated,"data":data_df.to_dict("records")}

            return data_to_send