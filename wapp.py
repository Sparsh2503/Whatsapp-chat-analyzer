import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


import pre_process, fetch
st.sidebar.title("Get your Chat Analysed")

uploaded_file = st.sidebar.file_uploader("Upload your file here")
if uploaded_file is not None:
    bd = uploaded_file.getvalue()
    data = bd.decode("utf-8")
    df = pre_process.preprocess(data)
    st.title('File Uploaded')



    user_list = df["user"].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    sel_user = st.sidebar.selectbox("show analysis of ", user_list)

    if st.sidebar.button("Show Analysis"):
        num_msgs , words , num_media , l = fetch.fetchdata(sel_user, df)
        st.title('Top Statistics')
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("no. of links shared")
            st.title(l)

        if sel_user == "Overall":
            col1 , col2 = st.columns(2)

            with col1:
                x = fetch.most_active(df)
                fig , ax = plt.subplots()

                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                a = round(((df["user"].value_counts().head())/df.shape[0])*100,2).reset_index().rename(columns = {"user":"Person","count":"Percent"})

                st.dataframe(a)
        st.title('Words used frequently')
        df_wc = fetch.wordcl(sel_user,df)

        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

# most common words
# first we have neglect all media omiited , stop words , group_notificaton which we have done in fetch.py
        col1,col2 = st.columns(2)

        with col1:
            w = fetch.word_count(sel_user,df)
            p = w.rename(columns={0:"word",1:"Count"})
            st.dataframe(p)

        with col2:
                wc = fetch.word_count(sel_user,df)
                fg,a = plt.subplots()
                a.bar(wc[0] , wc[1])
                plt.xticks(rotation = "vertical")
                st.pyplot(fg)
        st.title('Emojis used')
        col1 , col2 = st.columns(2)
        with col1:
            c = fetch.emoji_count(sel_user , df).rename(columns = {0 :"Emoji", 1 : "Count"})
            st.dataframe(c)

        with col2:
            c = fetch.emoji_count(sel_user, df).head(5)
            fig , ax = plt.subplots()
            ax.pie(c[1], labels = c[0] , autopct = '%0.2f')
            st.pyplot(fig)
        st.title('Activity')
        col1 , col2 = st.columns(2)


        with col1:
            a = fetch.activity(sel_user,df)

            st.dataframe(a)

        with col2:
            a = fetch.activity(sel_user,df)
            fig , ax = plt.subplots()
            ax.plot(a['time'],a['message'])
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)
