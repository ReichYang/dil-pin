from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
from google.cloud import vision
import io
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    #print('Labels:')

    #for label in labels:
    #    print(label.description)
    return labels


def detect_properties(path):
    """Detects image properties in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    return props


def get_properties_df(PATH):
    test_img = PATH
    test_prop = detect_properties(test_img)
    
    pixel_fractions = []
    for color in test_prop.dominant_colors.colors:
        pixel_fractions.append(color.pixel_fraction)
        
    color_arrs = []
    for color in test_prop.dominant_colors.colors:
        color_list = [color.color.red, color.color.green, color.color.blue]
        color_arrs.append(color_list)
        
    pixel_fractions_round = []
    for frac in pixel_fractions:
        pixel_fractions_round.append(int(frac * 100))
    
    colors_df = pd.DataFrame(color_arrs, index=pixel_fractions).reset_index()
    colors_df.rename(columns={'index': 'fraction'}, inplace=True)
    return colors_df

def get_properties_json(df_list):
    #takes list of dfs created by get_properties_df
    all_colors_df = pd.concat(df_list)
    all_colors_df.reset_index(inplace=True)
    all_colors_df.rename(columns={'index': 'img_index'}, inplace=True)
    all_colors_df.to_csv('property_colors.csv')
    
    all_color_list = []
    all_frac_list = []
    all_y_index_list = []

    for row in all_colors_df.iterrows():
        all_frac_list.append(row[1].fraction * 100)
        color_str = 'rgb(' + str(row[1][2]) + ', ' + str(row[1][3]) + ', ' + str(row[1][4]) + ')'
        all_color_list.append(color_str)
        all_y_index_list.append(row[1].img_index *14)

    color_dict = {
        'name': 'Colors',
        'data': []}

    for i in range(len(all_colors_df)):
        temp_dict = {'value': all_frac_list[i], 'color' : all_color_list[i]}
        color_dict['data'].append(temp_dict)

    return color_dict

def get_label_lists(paths):
    label_lists = []
    for path in paths:
        labels = detect_labels(path)
        labels_str = ''
        for label in labels:
            temp_label = str.lower(str(label.description))
            labels_str = labels_str + ' ' + str(temp_label)
        label_lists.append(labels_str)
    return label_lists

def get_label_vectors(label_lists):
    vectorizer = CountVectorizer(lowercase=False)
    vectors = vectorizer.fit_transform(label_lists).toarray()
    return vectors

def avg(items):
    sum = 0
    for item in items:
        #print(str(item))
        sum = sum + item
    if len(items) == 0:
        return 0
    return (sum / len(items))

def cossim(vectors): # number that match divided by total number possible
    return cosine_similarity(vectors)

def get_avg_cosine_sim(vectors):
    cos_matrix = cossim(vectors)
    
    score_list = []
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            if (i == j): # if not same post 
                score = cos_matrix[i][j]
                #print(str(score) + ' dropped')
            else:
                score = cos_matrix[i][j]
                score_list.append(score)

    return avg(score_list)

def gray_color_func(word, font_size, position, orientation, random_state,**kwargs):
    return (50,50,50)

def get_wordcloud(label_lists, search_term):

    concat_labels = ''
    for label_str in label_lists:
        concat_labels = concat_labels + ' ' + str(label_str)
        
    wordcloud = WordCloud(stopwords=[search_term], background_color='white', collocations=True, 
                        max_words=150, 
                        min_font_size=0, width= 320, height = 180
                        ).generate(concat_labels)
    plt.figure(figsize=[15,15])
    wordcloud.recolor(color_func=gray_color_func, random_state=9)
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
    return wordcloud

def get_desc_wordcloud(label_lists, search_term):

    concat_labels = ''
    for label_str in label_lists:
        concat_labels = concat_labels + ' ' + str(label_str)
        
    wordcloud = WordCloud(stopwords=search_term, background_color='white', collocations=True, 
                        max_words=150, 
                        min_font_size=0, width= 320, height = 180
                        ).generate(concat_labels)
    plt.figure(figsize=[15,15])
    wordcloud.recolor(color_func=gray_color_func, random_state=9)
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
    return wordcloud

def get_json_dict(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

def get_descripts(json):
    descript_list = []
    for pin in json:
        if 'description' in pin:
            descript_list.append(pin.get('description'))
    return descript_list

def get_domains(json):
    domain_list = []
    for pin in json:
        if 'domain' in pin:
            domain_list.append(pin.get('domain'))
    return domain_list

def get_boards(json):
    board_list = []
    for pin in json:
        if 'board' in pin:
            board_list.append(pin['board']['name'])
    return board_list

def get_promoters(json):
    promoter_list = []
    for pin in json:
        if 'promoter' in pin:
            if pin['promoter'] is not None:
                promoter_list.append(pin['promoter']['username'])
    return promoter_list

def get_dates(json):
    date_list = []
    for pin in json:
        if 'created_at' in pin:
            date = pin['created_at']
            date_list.append(pd.to_datetime(date))
    return date_list

def get_month(dt):
    return dt.month

def get_year(dt):
    return dt.year

def get_date_graph(dates):
    new_dates = []
    for date in dates:
        new_dates.append(date.to_pydatetime())
    df = pd.DataFrame(new_dates)
    df.rename(columns={0 : 'date'}, inplace=True)
    df["year"] = df["date"].map(get_year)
    df["month"] = df["date"].map(get_month)
    ax = df.groupby([df["year"]]).count().plot(kind="bar", color = '#ee9999')
    ax.legend_.remove()
    ax.set_title('Posts Per a Year')
    fig = ax.get_figure()
    return fig


