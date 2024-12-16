# URL & Content based Phishing Website Detection using Machine Learning 
**Team Member**: Haofei Ding
## 1. Problems
Phishing websites pose a significant threat to internet security by mimicking legitimate websites to steal sensitive information such as usernames and passwords. Traditional detection methods often rely on static patterns and rules, which can lead to high false-positive rates and ineffective defenses against new phishing strategies. This project focuses on developing a robust machine learning model to effectively detect phishing websites. In addition to extracting features from the URL itself, the model incorporates features such as webpage structure, content, and user interaction patterns for training. During this process, the most critical features for phishing detection are identified and classified. Finally, a browser plugin is developed to deploy the best-performing model for phishing detection.

## 2. Datasets

**Phishing URL Dataset**

The phishing URLs in this project are sourced from PhishTank, an open-source service that provides a comprehensive collection of phishing URLs in various formats such as CSV and JSON. This dataset is regularly updated to ensure the inclusion of the latest phishing threats. From PhishTank, I extracted **10,045** valid phishing URLs to train my machine learning models.(https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/dataset/phishing_websites.csv)

**Legitimate URL Dataset**

For legitimate websites, the dataset is obtained from Tranco, a reliable source that ranks websites based on their popularity and legitimacy. We collected **10,183** valid URLs from Tranco to ensure a balanced and comprehensive dataset for training. This dataset serves as a benchmark for identifying characteristics unique to legitimate websites, aiding in the accurate classification of URLs during model training.（https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/dataset/legitimate_websites.csv)

## 3. Approaches
### 3.1 Feature Extraction
In this project, the features are categorized into two main groups: URL-Based Features and Content-Based Features. The content-based features are further divided into Static Features (extracted using BeautifulSoup) and Dynamic Features (extracted using Selenium WebDriver). Below is a detailed breakdown:

**URL-Based Features (23 Features)**

A total of 23 features are extracted from the URLs to capture various characteristics that may indicate phishing activities. These include:

- Use of IP address in the URL
- Length and shortness of the URL
- Presence of special symbols and redirections
- Use of prefixes or suffixes in domain names
- Number of subdomains
- Domain registration length and use of non-standard ports
- HTTPS usage and abnormal URL patterns
- Website forwarding, status bar customization, and disabling right-click
- Use of pop-up windows and iframe redirection
- Age of domain, DNS records, website traffic, page rank, Google index status
Number of links pointing to the page and statistical reports

**Content-Based Features (50 Features)**

Content-based features focus on analyzing the structure, behavior, and interaction patterns of the webpage. These are divided into static and dynamic features:

1. Static HTML Features (Using BeautifulSoup). Static features are extracted from the HTML content to analyze the structure and elements of the webpage. These include:
- Presence of titles, submit buttons, links, email inputs
- Number of inputs, buttons, images, options, lists, hrefs, paragraphs, scripts
- Length of title and presence of header tags (h1, h2, h3)
- Length of text content and number of clickable buttons
- Presence of footer, forms, text areas, iframes, text inputs
- Number of meta tags, navigation elements, sources, spans, tables
- Specific URL requests like favicon links and anchor URLs

2. Dynamic Webpage Features ( Using Selenium WebDriver ). Features related to JavaScript behavior and user interaction are extracted. These include:
- Monitoring clipboard activity and form data collection
- Cookie manipulation and presence of mouse tracking or keyboard monitoring
- Use of pop-ups and number of hidden elements
- Page redirection behavior and external form actions
- Count of password types and names/IDs
- Hidden password fields and forms containing passwords

The extracted features can be categorized based on their distribution characteristics into two types: binary features with values of 0 or 1, and numerical features representing specific lengths or counts. During the subsequent training process, the numerical features are normalized to ensure consistency and improve model performance.

### 3.2 Training Models

Before starting the ML model training, the data is split into an 80-20 ratio. This dataset is used for a classification problem, where each input URL is classified as either phishing (1) or legitimate (0). The supervised machine learning models considered for training the dataset in this project are:  

1. K-Nearest Neighbors
2. Decision Tree
3. Random Forest
4. Gradient Boosting
5. Catboost
6. XGBoost

### 3.3 Develop Browser Extension

## 4. Experimental results
### Evaluation Metrics
#### **Precision**
  $$
  \text{Precision} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Positives (FP)}}
  $$
- **Interpretation**: Precision measures the proportion of true positive predictions out of all positive predictions made by the model. High precision indicates that when the model predicts a positive class, it is usually correct. It is crucial in scenarios where false positives are costly.

#### **Recall**
  $$
  \text{Recall} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Negatives (FN)}}
  $$
- **Interpretation**: Recall measures the proportion of true positive predictions out of all actual positive instances. High recall indicates that the model successfully identifies most of the actual positives. It is important in situations where missing true positives is costly.

#### **F1-Score**
  $$
  F1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
  $$
- **Interpretation**: The F1-score is the harmonic mean of precision and recall, providing a single metric to balance both. A high F1-score indicates a good balance between precision and recall, useful when both false positives and false negatives are equally important.

### **Support**
- **Definition**: Support refers to the number of actual occurrences of each class in the test data. It helps understand the distribution of classes in the dataset.

#### **Accuracy**
- **Definition**: 
- **Formula**:
  $$
  \text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Predictions}}
  $$
- **Interpretation**: Accuracy is the overall proportion of correct predictions made by the model. Accuracy provides a general measure of model performance but can be misleading in imbalanced datasets.

#### **Macro Average**
- **Definition**: Macro average calculates the average precision, recall, and F1-score equally across all classes, without considering class imbalance.
- **Use Case**: It treats all classes equally, which can be useful when class distribution is balanced or when each class's performance is equally important.

## 5. Future work


## 6. References
1. J. Mao, W. Tian, P. Li, T. Wei and Z. Liang, "Phishing-Alarm: Robust and Efficient Phishing Detection via Page Component Similarity," in IEEE Access, vol. 5, pp. 17020-17030, 2017, doi: 10.1109/ACCESS.2017.2743528.
2. S. Marchal, G. Armano, T. Gröndahl, K. Saari, N. Singh and N. Asokan, "Off-the-Hook: An Efficient and Usable Client-Side Phishing Prevention Application," in IEEE Transactions on Computers, vol. 66, no. 10, pp. 1717-1733, 1 Oct. 2017, doi: 10.1109/TC.2017.2703808.
3. Y. A. Alsariera, V. E. Adeyemo, A. O. Balogun and A. K. Alazzawi, "AI Meta-Learners and Extra-Trees Algorithm for the Detection of Phishing Websites," in IEEE Access, vol. 8, pp. 142532-142542, 2020, doi: 10.1109/ACCESS.2020.3013699.
4. A. Shrivastava, A. Raturi, A. Sharma, A. Rao, S. Singh and A. Sankhyan, "Phishing Website Detection Using Machine Learning," 2023 1st International Conference on Circuits, Power and Intelligent Systems (CCPIS), Bhubaneswar, India, 2023, pp. 1-6, doi: 10.1109/CCPIS59145.2023.10291190.
5. Choudhary, Tarun et al. “Machine Learning Approach for Phishing Attack Detection.” Journal of Artificial Intelligence and Technology (2023): n. pag.
6. M, D., Badkul, S., Gharat, K., Vidhate, A.V., & Bhosale, D. (2021). Detection of Phishing Websites Using Ensemble Machine Learning Approach. ITM Web of Conferences.
7. https://github.com/emre-kocyigit/phishing-website-detection-content-based
8. https://archive.ics.uci.edu/ml/datasets/Phishing+Websites.

## 7. Project Repository
https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning
