import streamlit as st
from urllib.parse import urlparse, parse_qs
from apiclient.discovery import build
import operator
import pandas as pd
from collections import Counter
from datetime import date
import seaborn as sns
from matplotlib import pyplot

# dd/mm/YY
today = date.today()
m = today.strftime("%m")   
y = today.strftime("%Y")
st.write("""### LEADERBOARD
 """)

API_KEY= "AIzaSyBZvr5x5TnXtF7enYpLMPY5xSat_G0x5VY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube= build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 developerKey=API_KEY,cache_discovery=False)

playlist_list=[]
video_id_list=[]
video_id_list1=[]
Dict_comments_count={}
Dict_comments_likes_count={}
Dict_replies_count={}
Author=[""]

#https://www.youtube.com/channel/UCiT9RITQ9PW6BhXK0y2jaeg
#https://www.youtube.com/channel/UCaKueGuXOEhblVVa7rCT2bA

def get_id(url):
    
    u_pars = urlparse(url)
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]


def leaderboard(df,x1,x2,x3):
	a4_dims=(10.7, 6.27)
	fig, ax1 = pyplot.subplots(figsize=a4_dims)

	ax=sns.barplot(y = 'Author',
            x = x1,
            data = df.head(20),palette="magma",ax=ax1)
	sns.set_style("whitegrid", {'grid.linestyle': '--'})
	#ax.grid(linestyle='-', linewidth='0.5', color='red')
	#ax.set_xlim((list(e.values())[19]-0)/2,list(e.values())[0])	
	# if(len(df)>19):
	# 	ax.set_xlim(int((df[df.index==19].values[0][1]-0)/2),int(df[df.index==0].values[0][1]))
	ax.set_title("{} {}".format(Author[0],x2), size=24)
	ax.set_xlabel(x3, size=16)
	ax.set_ylabel("Author", size=16)
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	#st.set_option('deprecation.showPyplotGlobalUse', False)
	st.pyplot()

def leaderboard_comments_counts(r1):
	sorted_d = dict( sorted(Dict_comments_count.items(), key=operator.itemgetter(1),reverse=True))
	df=pd.DataFrame(sorted_d.items(),columns=['Author', 'Count_of_Comments'])
	if(r1=="No" and Author[0] in df.values):
		df=df.drop(df[df["Author"] == Author[0]].index.tolist()[0],axis=0)
		
		
	leaderboard(df,'Count_of_Comments','Comment Leaderboard','Comment Count')

def leaderboard_comments_likes_counts(r1):
	sorted_d = dict( sorted(Dict_comments_likes_count.items(), key=operator.itemgetter(1),reverse=True))
	df=pd.DataFrame(sorted_d.items(),columns=['Author', 'Count_of_Comments_likes'])
	if(r1=="No" and Author[0] in df.values ):
		df=df.drop(df[df["Author"] == Author[0]].index.tolist()[0],axis=0)
	
	leaderboard(df,'Count_of_Comments_likes','Comment Like Leaderboard','Likes Count')

	
def leaderboard_replies_counts(r1):
	sorted_d = dict( sorted(Dict_replies_count.items(), key=operator.itemgetter(1),reverse=True))
	df=pd.DataFrame(sorted_d.items(),columns=['Author', 'Count_of_Replies'])
	if(r1=="No" and  Author[0] in df.values  ):
		df=df.drop(df[df["Author"] == Author[0]].index.tolist()[0],axis=0)
		
	leaderboard(df,'Count_of_Replies','Comment Reply Leaderboard','Reply Count')
	

def get_engagement_points():
    return Counter(Dict_comments_count) + Counter(Dict_comments_likes_count)+Counter(Dict_replies_count)

     
def leaderboard_engagement_points_counts(d,r1):
	sorted_d = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))
	df=pd.DataFrame(sorted_d.items(),columns=['Author', 'Count_of_engagement_points'])
	if(r1=="No" and  Author[0] in df.values ):
		df=df.drop(df[df["Author"] == Author[0]].index.tolist()[0],axis=0)
	
	leaderboard(df,'Count_of_engagement_points','Engagement Point Leaderboard','Engagement Points')
	
def get_author_of_comments_count(r2):
	count=0
	count2=0
	for i in range(len(video_id_list)):
		response2=youtube.commentThreads().list(part="snippet",videoId=video_id_list[i],maxResults=90).execute()

		while(response2):
			for item in response2['items']:
				dat=item['snippet']["topLevelComment"]['snippet']['updatedAt']
				d=dat.split('-')
				month=d[1]
				year=d[0]
				if((r2=="This Month" and year==y and month==m) or(r2=="This Year" and year==y )):
					count=count+1
					author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
					Dict_comments_count[author]=Dict_comments_count.get(author,0)+1
					like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
					Dict_comments_likes_count[author]=Dict_comments_likes_count.get(author,0)+like_count
					count2=count2+like_count
				
				
			if 'nextPageToken' in response2:
				response2 = youtube.commentThreads().list(part="snippet",videoId=video_id_list[i],maxResults=90,pageToken=response2['nextPageToken']).execute()
			else:
				break

def get_author_of_replies_count(r2):
	count=0
	count2=0
	for i in range(len(video_id_list)):
		response2=youtube.commentThreads().list(part='snippet,replies',videoId=video_id_list[i],maxResults=90).execute()
		while(response2):
			for item in range(0,len(response2['items'])):
				try:
					for j in range(0,len(response2['items'][item]['replies']['comments'])):
						dat=author = response2['items'][item]['replies']['comments'][j]['snippet']['updatedAt']
						d=dat.split('-')
						month=d[1]
						year=d[0]
						if((r2=="This Month" and year==y and month==m) or(r2=="This Year" and year==y )):
							author = response2['items'][item]['replies']['comments'][j]['snippet']['authorDisplayName']
							Dict_replies_count[author]=Dict_replies_count.get(author,0)+1
				except:
					continue
			if 'nextPageToken' in response2:
				response2 = youtube.commentThreads().list(part='snippet,replies',videoId='myhoWUrSP7o',maxResults=90,pageToken=response2['nextPageToken']).execute()
			else:
				break
		
	

def videoId(r2):
	count=0
	for i in range(len(playlist_list)):
		response2=youtube.playlistItems().list(part="snippet",playlistId=playlist_list[i],maxResults=40).execute()
		
		while(response2):
			for item in response2['items']:
				video_id_list1.append(item['snippet']["resourceId"]["videoId"])
			if 'nextPageToken' in response2:
				response2 = youtube.playlistItems().list(part="snippet",playlistId=playlist_list[i],maxResults=40,pageToken=response2['nextPageToken']).execute()
			else:
				break
	for i in set(video_id_list1):
		video_id_list.append(i)
	
flag=[0]
def build_service():
    link=st.text_input("YOUTUBE CHANNEL LINK   (eg -> https://www.youtube.com/channel/******************* )")
    response=""
    count=0
    if(not link):

        return 
    try:
    	Id=get_id(link)
    	response2=youtube.channels().list(part='snippet',id=Id,maxResults=40).execute()
    	Author.insert(0,response2['items'][0]['snippet']['title'])
    	response=youtube.playlists().list(part="snippet",channelId=Id,maxResults=40).execute()
    	flag.insert(0,1)
    	
    except:
    	st.error( "Incorrect Link")

    
    while(response):
        for item in response['items']:
            playlist_list.append(item["id"])
            count=count+1
            
            

        if 'nextPageToken' in response:
            response = youtube.playlists().list(part="snippet",channelId=Id,maxResults=40,pageToken=response['nextPageToken']).execute()
        else:
            break
    

    


build_service()
r1=st.sidebar.radio("Include Author --> {}".format(Author[0]),["Yes","No"])
r2=st.sidebar.radio("Time Period",["This Year","This Month"])
videoId(r2)
get_author_of_comments_count(r2)
get_author_of_replies_count(r2)

if(len(Dict_comments_count)<1 and flag[0]==1):
	st.write("No comments {}".format(r2))
# try:
if(len(Dict_comments_count)>=1 and flag[0]==1):
	option = st.selectbox(
     'Select which leaderboard you want to see',
     ('Engagement Points', 'Likes', '# of Comments','Replies'))
	if option == '# of Comments':
		leaderboard_comments_counts(r1)
	elif option=='Likes' :
		leaderboard_comments_likes_counts(r1)
	elif option=='Replies':
		leaderboard_replies_counts(r1)
	elif option=='Engagement Points':
		d=get_engagement_points()
		leaderboard_engagement_points_counts(d,r1)
# except:
# 	pass
