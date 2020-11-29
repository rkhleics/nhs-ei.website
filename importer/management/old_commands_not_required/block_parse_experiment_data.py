""" 
    a_to_z_index_component # leave out

    article_component 
        article_title
        article_content
        article_url
        
    in_this_section_component
        in_this_section_title
        in_this_section_topics [
            in_this_section_link_title, 
            in_this_section_link_url
        ]

    priorities_component
        priorities_section_title
        our_priorities [
            priority_title, priority_url
        ]

    recent_posts_component
        section_title
        post_type
        number_of_posts
        show_see_all
        select_category [
            category ids
        ]

    promos_component 
        promo_component [
            promo_image: {
                id
            }
            promo_title
            promo_content
            promo_url
        ] 

        
    topic_section_component
        topic_section_title
        in_this_section [
            topic_title
            topic_content
            topic_url
        ]
"""


""" topic_section_component, priorities_component, in_this_section_component, recent_posts_component, promos_component"""
DATA_ALL = "[\
    {'acf_fc_layout': 'a_to_z_index_component', \
        'a_to_z_index_title': 'A to Z of topics', \
        'a_to_z_index_content': '<p>Can’t find what you’re looking for? Our A to Z of topics helps you find information quickly:</p>\\n'},\
    {'acf_fc_layout': 'topic_section_component', \
        'topic_section_title': '', 'in_this_section': \
        [\
            {\
            'topic_title': 'About the Involvement Hub', \
            'topic_content': '<p>A source of information for people who want to get involved in our work or enable others to participate.</p>\\n', \
            'topic_url': 'https://www.england.nhs.uk/participation/about/'\
            }, {'topic_title': 'Information for commissioners', 'topic_content': '<p>Statutory guidance for Clinical Commissioning Groups on involving patients and the public.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/involvementguidance'}, {'topic_title': 'Surveys and consultations', 'topic_content': '<p>Have your say on our current consultations and surveys.</p>\\n', 'topic_url': 'https://www.engage.england.nhs.uk/'}, {'topic_title': 'Learning and development', 'topic_content': '<p>Workshops, webinars and elearning to improve understanding of the healthcare sector and participation.  </p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/learning/'}, {'topic_title': 'Good practice and case studies', 'topic_content': '<p>Examples of good practice in involving people in healthcare services and service development.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/success/'}, {'topic_title': 'Resources and bite sized guides', 'topic_content': '<p>A variety of resources to support you in your involvement work, including bitesize guides to participation.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/resources/'}]}, \
                \
    {'acf_fc_layout': 'priorities_component', 'priorities_section_title': '', 'our_priorities': \
        [\
            {\
                'nhsuk_highlight': False, \
                'priority_title': 'How to get involved', \
                'priority_url': 'https://www.england.nhs.uk/participation/get-involved/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Why get involved', 'priority_url': 'https://www.england.nhs.uk/participation/why/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Current opportunities', 'priority_url': 'https://www.england.nhs.uk/participation/get-involved/opportunities/'}]}, \
                \
    {'acf_fc_layout': 'in_this_section_component', \
        'in_this_section_title': 'You may also be interested in', \
        'in_this_section_topics': [\
            {\
                'type': 'link', \
                'in_this_section_link_title': '1 An introduction to the NHS', \
                'in_this_section_link_url': 'https://www.england.nhs.uk/participation/nhs/', \
                'in_this_section_page': False\
            },\
                {\
                'type': 'link', \
                'in_this_section_link_title': '2 An introduction to the NHS', \
                'in_this_section_link_url': 'https://www.england.nhs.uk/participation/nhs/', \
                'in_this_section_page': False\
            },\
                {\
                'type': 'link', \
                'in_this_section_link_title': '3 An introduction to the NHS', \
                'in_this_section_link_url': 'https://www.england.nhs.uk/participation/nhs/', \
                'in_this_section_page': False\
            }\
        ]\
    }, \
    {'acf_fc_layout': 'recent_posts_component', \
        'section_title': 'News and blogs', \
            'post_type': ['blog', 'post'], \
            'number_of_posts': '3', \
            'show_see_all': True, \
            'select_category': [2687], \
            'background': True, \
            'background_colour': '#e8edee'}, \
    {'acf_fc_layout': 'promos_component', 'promo_component': \
        [\
            {\
                'nhsuk_highlight': False, \
                'promo_image': {\
                    'ID': 129988, \
                    'id': 129988, \
                    'title': 'surgeons-400x267', \
                    'filename': 'surgeons-400x267.jpg', \
                    'filesize': 117610, \
                    'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                    'link': 'https://www.england.nhs.uk/ourwork/surgeons-400x267/', \
                    'alt': 'Surgeons operate on a patient', \
                    'author': '1904', \
                    'description': '', \
                    'caption': '', \
                    'name': 'surgeons-400x267', \
                    'status': 'inherit', \
                    'uploaded_to': 15136, \
                    'date': '2019-01-09 10:43:53', \
                    'modified': '2019-01-09 10:45:30', \
                    'menu_order': 0, \
                    'mime_type': 'image/jpeg', \
                    'type': 'image', \
                    'subtype': 'jpeg', \
                    'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', \
                    'width': 400, \
                    'height': 267, \
                    'sizes': {\
                        'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267-150x150.jpg', \
                        'thumbnail-width': 150, \
                        'thumbnail-height': 150, \
                        'medium': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267-300x200.jpg', \
                        'medium-width': 300, \
                        'medium-height': 200, \
                        'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                        'medium_large-width': 400, \
                        'medium_large-height': 267, \
                        'large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                        'large-width': 400, \
                        'large-height': 267, \
                        '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                        '1536x1536-width': 400, \
                        '1536x1536-height': 267, \
                        '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                        '2048x2048-width': 400, '2048x2048-height': 267\
                    }\
                }, \
                'promo_title': 'NHS Long Term Plan', \
                'promo_content': '', \
                'promo_url': 'https://www.england.nhs.uk/long-term-plan/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 78273, 'id': 78273, 'title': '', 'filename': 'cancer_400x267.jpg', 'filesize': 149433, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'link': 'https://www.england.nhs.uk/?attachment_id=78273', 'alt': 'Two women taking part in a fundraising event', 'author': '1920', 'description': '', 'caption': '', 'name': 'muddy-fundraising', 'status': 'inherit', 'uploaded_to': 78255, 'date': '2017-02-08 13:49:56', 'modified': '2017-10-09 14:18:57', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Cancer', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/cancer/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 78275, 'id': 78275, 'title': '', 'filename': 'mental-health-and-dementia_400x267.jpg', 'filesize': 127258, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'link': 'https://www.england.nhs.uk/?attachment_id=78275', 'alt': 'A father and son read a letter', 'author': '1920', 'description': '', 'caption': '', 'name': 'relation-between-father-and-son', 'status': 'inherit', 'uploaded_to': 78255, 'date': '2017-02-08 13:50:41', 'modified': '2017-10-09 14:19:14', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Mental health', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/mental-health/'}]}, \
    {'acf_fc_layout': 'article_component', \
        'article_image': {\
            'ID': 163377, \
            'id': 163377, \
            'title': 'Clear on cancer', \
            'filename': 'Clear-on-cancer.jpg', \
            'filesize': 137636, \
            'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
            'link': 'https://www.england.nhs.uk/homepage/clear-on-cancer/', \
            'alt': 'Help Us, Help you', 'author': '2119', 'description': '', 'caption': '', \
            'name': 'clear-on-cancer', 'status': 'inherit', 'uploaded_to': 98164, \
            'date': '2020-10-09 16:07:59', 'modified': '2020-10-09 16:08:19', \
            'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', \
            'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 455, 'height': 487, \
            'sizes': {\
                'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-150x150.jpg', \
                'thumbnail-width': 150, 'thumbnail-height': 150, \
                'medium': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-280x300.jpg', \
                'medium-width': 280, 'medium-height': 300, \
                'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                'medium_large-width': 455, 'medium_large-height': 487, \
                'large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                'large-width': 455, 'large-height': 487, \
                '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                '1536x1536-width': 455, '1536x1536-height': 487, \
                '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                '2048x2048-width': 455, '2048x2048-height': 487\
            }, \
        }, \
        'article_image_alignment': 'has-left-aligned-image', \
        'article_image_size': 'has-zero-width-image', \
        'article_background': False, \
        'article_background_colour': '', \
        'article_title': '', \
        'article_content': '<p>article 2NHS England and NHS Improvement leads the National Health Service (NHS) in England, find out more about what we do:</p>\\n', \
        'article_url': ''}, \
    {'acf_fc_layout': 'article_component', \
        'article_image': False, \
        'article_image_alignment': 'has-left-aligned-image', \
        'article_image_size': 'has-zero-width-image', \
        'article_background': False, \
        'article_background_colour': '', \
        'article_title': '', \
        'article_content': '<p>article 3NHS England and NHS Improvement leads the National Health Service (NHS) in England, find out more about what we do:</p>\\n', \
        'article_url': ''}, \
    ]"

DATA_1 = "[\
    {'acf_fc_layout': 'topic_section_component', 'topic_section_title': '', 'in_this_section': \
        [\
            {\
            'topic_title': 'About the Involvement Hub', \
            'topic_content': '<p>A source of information for people who want to get involved in our work or enable others to participate.</p>\\n', \
            'topic_url': 'https://www.england.nhs.uk/participation/about/'\
            }, {'topic_title': 'Information for commissioners', 'topic_content': '<p>Statutory guidance for Clinical Commissioning Groups on involving patients and the public.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/involvementguidance'}, {'topic_title': 'Surveys and consultations', 'topic_content': '<p>Have your say on our current consultations and surveys.</p>\\n', 'topic_url': 'https://www.engage.england.nhs.uk/'}, {'topic_title': 'Learning and development', 'topic_content': '<p>Workshops, webinars and elearning to improve understanding of the healthcare sector and participation.  </p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/learning/'}, {'topic_title': 'Good practice and case studies', 'topic_content': '<p>Examples of good practice in involving people in healthcare services and service development.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/success/'}, {'topic_title': 'Resources and bite sized guides', 'topic_content': '<p>A variety of resources to support you in your involvement work, including bitesize guides to participation.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/participation/resources/'}]}, \
                \
    {'acf_fc_layout': 'priorities_component', 'priorities_section_title': '', 'our_priorities': \
        [\
            {\
                'nhsuk_highlight': False, \
                'priority_title': 'How to get involved', \
                'priority_url': 'https://www.england.nhs.uk/participation/get-involved/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Why get involved', 'priority_url': 'https://www.england.nhs.uk/participation/why/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Current opportunities', 'priority_url': 'https://www.england.nhs.uk/participation/get-involved/opportunities/'}]}, \
                \
    {'acf_fc_layout': 'in_this_section_component', 'in_this_section_title': 'You may also be interested in', 'in_this_section_topics': [{'type': 'link', 'in_this_section_link_title': 'An introduction to the NHS', 'in_this_section_link_url': 'https://www.england.nhs.uk/participation/nhs/', 'in_this_section_page': False}]}, \
        \
    {'acf_fc_layout': 'recent_posts_component', 'section_title': 'News and blogs', 'post_type': ['blog', 'post'], 'number_of_posts': '3', 'show_see_all': True, 'select_category': [2687], 'background': True, 'background_colour': '#e8edee'}, \
    \
    {'acf_fc_layout': 'promos_component', 'promo_component': \
        [\
            {'nhsuk_highlight': False, 'promo_image': {'ID': 131123, 'id': 131123, 'title': 'intouch-banner-3', 'filename': 'intouch-banner-3.png', 'filesize': 315683, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3.png', 'link': 'https://www.england.nhs.uk/homepage/intouch-banner-3/', 'alt': 'Signup to receive the In touch bulletin', 'author': '1849', 'description': '', 'caption': '', 'name': 'intouch-banner-3', 'status': 'inherit', 'uploaded_to': 98164, 'date': '2019-01-29 18:43:47', 'modified': '2019-01-29 18:44:19', 'menu_order': 0, 'mime_type': 'image/png', 'type': 'image', 'subtype': 'png', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 1200, 'height': 263, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3-150x150.png', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3-300x66.png', 'medium-width': 300, 'medium-height': 66, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3-768x168.png', 'medium_large-width': 768, 'medium_large-height': 168, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3-1024x224.png', 'large-width': 1024, 'large-height': 224, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3.png', '1536x1536-width': 1200, '1536x1536-height': 263, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/intouch-banner-3.png', '2048x2048-width': 1200, '2048x2048-height': 263}}, 'promo_title': '', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/email-bulletins/in-touch-bulletin/'}]}]"


"""article_component, promos_component, priorities_component, a_to_z_index_component"""

DATA_2 = "[\
    {'acf_fc_layout': 'article_component', \
        'article_image': {\
            'ID': 163377, \
            'id': 163377, \
            'title': 'Clear on cancer', \
            'filename': 'Clear-on-cancer.jpg', \
            'filesize': 137636, \
            'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
            'link': 'https://www.england.nhs.uk/homepage/clear-on-cancer/', \
            'alt': 'Help Us, Help you', 'author': '2119', 'description': '', 'caption': '', \
            'name': 'clear-on-cancer', 'status': 'inherit', 'uploaded_to': 98164, \
            'date': '2020-10-09 16:07:59', 'modified': '2020-10-09 16:08:19', \
            'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', \
            'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 455, 'height': 487, \
            'sizes': {\
                'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-150x150.jpg', \
                'thumbnail-width': 150, 'thumbnail-height': 150, \
                'medium': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-280x300.jpg', \
                'medium-width': 280, 'medium-height': 300, \
                'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                'medium_large-width': 455, 'medium_large-height': 487, \
                'large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                'large-width': 455, 'large-height': 487, \
                '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                '1536x1536-width': 455, '1536x1536-height': 487, \
                '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', \
                '2048x2048-width': 455, '2048x2048-height': 487\
            }, \
        }, \
        'article_image_alignment': 'has-left-aligned-image', \
        'article_image_size': 'has-zero-width-image', \
        'article_background': False, \
        'article_background_colour': '', \
        'article_title': '', \
        'article_content': '<p>NHS England and NHS Improvement leads the National Health Service (NHS) in England, find out more about what we do:</p>\\n', \
        'article_url': ''}, \
    {'acf_fc_layout': 'promos_component', 'promo_component': \
        [\
            {\
                'nhsuk_highlight': False, \
                'promo_image': {\
                    'ID': 129988, \
                    'id': 129988, \
                    'title': 'surgeons-400x267', \
                    'filename': 'surgeons-400x267.jpg', \
                    'filesize': 117610, \
                    'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', \
                    'link': 'https://www.england.nhs.uk/ourwork/surgeons-400x267/', \
                    'alt': 'Surgeons operate on a patient', \
                    'author': '1904', \
                    'description': '', \
                    'caption': '', \
                    'name': 'surgeons-400x267', \
                    'status': 'inherit', \
                    'uploaded_to': 15136, \
                    'date': '2019-01-09 10:43:53', \
                    'modified': '2019-01-09 10:45:30', \
                    'menu_order': 0, \
                    'mime_type': 'image/jpeg', \
                    'type': 'image', \
                    'subtype': 'jpeg', \
                    'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', \
                    'width': 400, \
                    'height': 267, \
                    'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2019/01/surgeons-400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'NHS Long Term Plan', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/long-term-plan/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 78273, 'id': 78273, 'title': '', 'filename': 'cancer_400x267.jpg', 'filesize': 149433, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'link': 'https://www.england.nhs.uk/?attachment_id=78273', 'alt': 'Two women taking part in a fundraising event', 'author': '1920', 'description': '', 'caption': '', 'name': 'muddy-fundraising', 'status': 'inherit', 'uploaded_to': 78255, 'date': '2017-02-08 13:49:56', 'modified': '2017-10-09 14:18:57', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/cancer_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Cancer', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/cancer/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 78275, 'id': 78275, 'title': '', 'filename': 'mental-health-and-dementia_400x267.jpg', 'filesize': 127258, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'link': 'https://www.england.nhs.uk/?attachment_id=78275', 'alt': 'A father and son read a letter', 'author': '1920', 'description': '', 'caption': '', 'name': 'relation-between-father-and-son', 'status': 'inherit', 'uploaded_to': 78255, 'date': '2017-02-08 13:50:41', 'modified': '2017-10-09 14:19:14', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/02/mental-health-and-dementia_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Mental health', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/mental-health/'}]}, \
    {'acf_fc_layout': 'promos_component', 'promo_component': \
        [\
            {'nhsuk_highlight': False, 'promo_image': {'ID': 88622, 'id': 88622, 'title': '', 'filename': 'urgent-and-emergency-care_400x267.jpg', 'filesize': 103334, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267.jpg', 'link': 'https://www.england.nhs.uk/ourwork/ambulance-crew-pulling-stretcher/', 'alt': 'An ambulance crew pulling a stretcher', 'author': '1904', 'description': '', 'caption': '', 'name': 'ambulance-crew-pulling-stretcher', 'status': 'inherit', 'uploaded_to': 15136, 'date': '2017-03-29 13:06:38', 'modified': '2017-10-09 14:19:22', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/urgent-and-emergency-care_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Urgent and emergency care', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/urgent-emergency-care/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 88618, 'id': 88618, 'title': '', 'filename': 'primary-care_400x267.jpg', 'filesize': 104232, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267.jpg', 'link': 'https://www.england.nhs.uk/five-year-forward-view/next-steps-on-the-nhs-five-year-forward-view/doctor-chatting-to-male-patient-2/', 'alt': 'A doctor in discussion with a patient', 'author': '1904', 'description': '', 'caption': '', 'name': 'doctor-chatting-to-male-patient-2', 'status': 'inherit', 'uploaded_to': 88790, 'date': '2017-03-29 13:06:19', 'modified': '2019-03-11 15:40:55', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/03/primary-care_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Primary care', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/primary-care/'}, \
            {'nhsuk_highlight': False, 'promo_image': {'ID': 88505, 'id': 88505, 'title': '', 'filename': 'patients-01_400x267.jpg', 'filesize': 121593, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267.jpg', 'link': 'https://www.england.nhs.uk/ourwork/baby-clinic-visit-for-toddler-and-mum-3/', 'alt': 'A mother and child chat with a nurse', 'author': '1920', 'description': '', 'caption': '', 'name': 'baby-clinic-visit-for-toddler-and-mum-3', 'status': 'inherit', 'uploaded_to': 15136, 'date': '2017-03-28 14:34:08', 'modified': '2017-10-09 14:19:50', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 400, 'height': 267, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267-300x200.jpg', 'medium-width': 300, 'medium-height': 200, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267.jpg', 'medium_large-width': 400, 'medium_large-height': 267, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267.jpg', 'large-width': 400, 'large-height': 267, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267.jpg', '1536x1536-width': 400, '1536x1536-height': 267, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2012/10/patients-01_400x267.jpg', '2048x2048-width': 400, '2048x2048-height': 267}}, 'promo_title': 'Integrated care', 'promo_content': '', 'promo_url': 'https://www.england.nhs.uk/integratedcare/'}]}, \
    {'acf_fc_layout': 'priorities_component', 'priorities_section_title': '', 'our_priorities': \
        [\
            {'nhsuk_highlight': False, 'priority_title': 'NHS Diabetes Prevention Programme (NHS DPP)', 'priority_url': 'https://www.england.nhs.uk/diabetes/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Nursing, midwifery and care staff', 'priority_url': 'https://www.england.nhs.uk/nursingmidwifery/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Clinical review of NHS access standards', 'priority_url': 'https://www.england.nhs.uk/clinically-led-review-nhs-access-standards/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'NHS Standard Contract ', 'priority_url': 'https://www.england.nhs.uk/nhs-standard-contract/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'NHS RightCare', 'priority_url': 'https://www.england.nhs.uk/rightcare/'}, \
            {'nhsuk_highlight': False, 'priority_title': 'Learning disability and autism', 'priority_url': 'https://www.england.nhs.uk/learning-disabilities/'}]}, \
    {'acf_fc_layout': 'a_to_z_index_component', 'a_to_z_index_title': 'A to Z of topics', 'a_to_z_index_content': '<p>Can’t find what you’re looking for? Our A to Z of topics helps you find information quickly:</p>\\n'}]"

"""promos_component, topic_section_component, in_this_section_component"""

DATA_3 = "[\
    {'acf_fc_layout': 'promos_component', 'promo_component': \
        [{'nhsuk_highlight': False, 'promo_image': {'ID': 102119, 'id': 102119, 'title': '', 'filename': 'about-us_1200x300.jpg', 'filesize': 265121, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300.jpg', 'link': 'https://www.england.nhs.uk/about/medical-staff-having-meeting-at-nurse-station/', 'alt': '', 'author': '1920', 'description': '', 'caption': '', 'name': 'medical-staff-having-meeting-at-nurse-station', 'status': 'inherit', 'uploaded_to': 991, 'date': '2017-08-23 10:43:55', 'modified': '2018-09-13 14:41:24', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 1200, 'height': 300, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300-300x75.jpg', 'medium-width': 300, 'medium-height': 75, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300-768x192.jpg', 'medium_large-width': 768, 'medium_large-height': 192, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300-1024x256.jpg', 'large-width': 1024, 'large-height': 256, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300.jpg', '1536x1536-width': 1200, '1536x1536-height': 300, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2017/08/about-us_1200x300.jpg', '2048x2048-width': 1200, '2048x2048-height': 300}}, 'promo_title': '', 'promo_content': '', 'promo_url': ''}]}, \
    {'acf_fc_layout': 'topic_section_component', 'topic_section_title': '', 'in_this_section': \
        [{'topic_title': 'What do we do?', 'topic_content': '<p>NHS England and NHS Improvement leads the National Health Service (NHS) in England, find out more about what we do.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/about/about-nhs-england'}, {'topic_title': 'Our Board', 'topic_content': '<p>Find out about our Board, its members, its roles and responsibilities and dates of future meetings.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/about/board/'}, {'topic_title': 'Corporate publications', 'topic_content': '<p>Read our annual report, business plan, financial performance reports and the Five Year Forward View.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/publications'}, {'topic_title': 'Regional teams', 'topic_content': '<p>There are seven regional teams that support the commissioning of healthcare services for different parts of the country.</p>\\n', 'topic_url': 'https://www.england.nhs.uk/about/regional-area-teams/'}, {'topic_title': 'Our work', 'topic_content': \"<p>Learn about what we're doing in cancer, primary care, mental health,  urgent and emergency care and other key areas.</p>\\n\", 'topic_url': 'https://www.england.nhs.uk/ourwork'}]}, \
    {'acf_fc_layout': 'in_this_section_component', 'in_this_section_title': 'You may also be interested in', 'in_this_section_topics': [{'type': 'link', 'in_this_section_link_title': 'Sustainable development', 'in_this_section_link_url': 'https://www.england.nhs.uk/about/sustainable-development/', 'in_this_section_page': False}, {'type': 'link', 'in_this_section_link_title': 'Working for us', 'in_this_section_link_url': 'https://www.england.nhs.uk/about/working-for/', 'in_this_section_page': False}, {'type': 'link', 'in_this_section_link_title': 'Contact us', 'in_this_section_link_url': 'https://www.england.nhs.uk/contact-us/', 'in_this_section_page': False}, {'type': 'link', 'in_this_section_link_title': 'Equality, diversity and health inequalities', 'in_this_section_link_url': 'https://www.england.nhs.uk/about/equality/', 'in_this_section_page': False}]}]"

"""
#DATA_HOME_PAGE = '[{'acf_fc_layout': 'article_component', 'article_image': {'ID': 163377, 'id': 163377, 'title': 'Clear on cancer', 'filename': 'Clear-on-cancer.jpg', 'filesize': 137636, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', 'link': 'https://www.england.nhs.uk/homepage/clear-on-cancer/', 'alt': 'Help Us, Help you', 'author': '2119', 'description': '', 'caption': '', 'name': 'clear-on-cancer', 'status': 'inherit', 'uploaded_to': 98164, 'date': '2020-10-09 16:07:59', 'modified': '2020-10-09 16:08:19', 'menu_order': 0, 'mime_type': 'image/jpeg', 'type': 'image', 'subtype': 'jpeg', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/default.png', 'width': 455, 'height': 487, 'sizes': {'thumbnail': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-150x150.jpg', 'thumbnail-width': 150, 'thumbnail-height': 150, 'medium': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer-280x300.jpg', 'medium-width': 280, 'medium-height': 300, 'medium_large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', 'medium_large-width': 455, 'medium_large-height': 487, 'large': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', 'large-width': 455, 'large-height': 487, '1536x1536': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', '1536x1536-width': 455, '1536x1536-height': 487, '2048x2048': 'https://www.england.nhs.uk/wp-content/uploads/2020/10/Clear-on-cancer.jpg', '2048x2048-width': 455, '2048x2048-height': 487}}, 'article_image_alignment': 'has-left-aligned-image', 'article_image_size': 'has-half-width-image', 'article_background': False, 'article_background_colour': '#e8edee', 'article_title': 'Help Us, Help You - Accessing NHS Services campaign', 'article_content': '<p>The NHS has introduced a range of measures to ensure the safety of patients and the ‘Help Us, Help You’ campaign will help to reassure them they can receive medical care safely. This new campaign launched in October, to address the barriers deterring people from accessing NHS services during the pandemic.</p>\n<p>The first phase of the campaign encourages people to contact their GP if they are worried about a <a href="https://www.nhs.uk/conditions/cancer/symptoms/">symptom that could be cancer</a>.\xa0Further phases will remind pregnant women to attend check-ups and seek advice if they are worried about their baby, ask patients to keep their routine elective appointments, and encourage those with mental health issues to access NHS support.</p>\n<p><strong>Your NHS is here to see you, safely. </strong></p>\n<p>Stakeholders, partners and regional teams can access resources to help them support the campaign via the <a href="https://campaignresources.phe.gov.uk/resources/campaigns/113-help-us">Campaign Resource Centre</a>.</p>\n', 'article_url': 'https://www.england.nhs.uk/2020/10/celebs-and-lockdown-heroes-urge-public-to-get-cancer-symptoms-checked-and-attend-routine-appointments/'}, {'acf_fc_layout': 'article_component', 'article_image': False, 'article_image_alignment': 'has-left-aligned-image', 'article_image_size': 'has-zero-width-image', 'article_background': True, 'article_background_colour': '#e8edee', 'article_title': 'How could this website work better for you?', 'article_content': '<p>We are building a new single website for NHS England and NHS Improvement. In the meantime, you can find information on both providers and commissioned healthcare services on this website.</p>\n<p>We want to understand how you’re using our website so we can make the new one better. Please\xa0<a href="https://www.england.nhs.uk/contact-us/feedback/">fill out this short form</a>\xa0if you’d like to improve the site.</p>\n', 'article_url': ''}]'
"""