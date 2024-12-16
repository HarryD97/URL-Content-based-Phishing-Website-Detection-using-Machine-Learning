# Introduction
1. Install the library from requirements.txt.
2. Run websites_collections.py (https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/dataset/websites_collection.py) to crawl data with the URLs from verified_online.csv and tranco_list.csv.
3. Follow Training.ipynb (https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Model/Training.ipynb) to train ML models.
4. Run app.py to deploy the model (I used the only Top 20 features to build the model for the chrome extension ).
5. Deploy the chrome extension by selecting the whole folder "Google Extension".
    ![](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/extension.png?raw=t)
# Final Report:
##  URL & Content based Phishing Website Detection using Machine Learning   
**Team Member & Author**: Haofei Ding  
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
  
####   3.2.1 K-Nearest Neighbors (KNN)
KNN is a simple, non-parametric algorithm used for classification and regression tasks. It classifies data points based on the majority vote of their neighbors, with the data point being assigned to the class most common among its k nearest neighbors, as determined by a distance metric like Euclidean distance. 
![](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/output.png?raw=t)
Best n_neighbors Value: 1
|            | Precision | Recall  | F1-Score |
|------------|-----------|---------|----------|
| 0          | 0.957086  | 0.948566| 0.952807 |
| 1          | 0.949070  | 0.957510| 0.953271 |
| Accuracy   | 0.953040  ||
| Macro Avg  | 0.953078  | 0.953038| 0.953039 |


#### 3.2.2 Decision Tree
A decision tree is a non-parametric supervised learning algorithm that can be used for both classification and regression tasks. It splits the data into subsets based on the value of input features, forming a tree-like structure where each node represents a decision based on an attribute, and each branch represents the outcome of that decision. Decision trees are intuitive and easy to interpret, allowing for clear visualization of decision-making processes. They handle both numerical and categorical data well.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/DTCV.png?raw=tr)
Best max_depth: 29
|            | Precision | Recall    | F1-Score  |
|------------|-----------|-----------|-----------|
| 0          | 0.958146  | 0.951039  | 0.954579  |
| 1          | 0.951447  | 0.958498  | 0.954959  |
| Accuracy   | 0.954770  | |
| Macro Avg  | 0.954797  | 0.954768  | 0.954769  |

#### 3.2.3 Random Forest 
Random Forest is an ensemble learning method that constructs multiple decision trees during training and outputs the mode of their predictions for classification tasks. It reduces overfitting by averaging multiple decision trees, thus improving accuracy and robustness. Random Forest is versatile and performs well with large datasets but can be computationally intensive. Random Forest is particularly useful for handling large datasets with many features, as it can automatically manage feature importance and interactions, leading to better generalization across diverse phishing tactics.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/RFCV.png?raw=tr)
Best n_estimators: 22
|            | Precision | Recall    | F1-Score  |
|------------|-----------|-----------|-----------|
| 0          | 0.968535  | 0.974283  | 0.971400  |
| 1          | 0.974155  | 0.968379  | 0.971259  |
| Accuracy   | 0.971330  | 
| Macro Avg  | 0.971345  | 0.971331  | 0.971330  |

#### 3.2.4 Gradient Boosting
Gradient Boosting is an iterative method that builds a model in stages by optimizing a loss function. It combines multiple weak learners, usually decision trees, to create a strong predictive model by sequentially correcting the errors made by previous models.  This model is beneficial when you need a high-performing classifier that can adapt to subtle patterns in the data, such as those found in evolving phishing strategies.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/GBCV.png?raw=tr)
Best Learning Rate: 0.9
|            | Precision | Recall    | F1-Score  |
|------------|-----------|-----------|-----------|
| 0          | 0.963910  | 0.951039  | 0.957431  |
| 1          | 0.951731  | 0.964427  | 0.958037  |
| Accuracy   | 0.957736  |  |
| Macro Avg  | 0.957820  | 0.957733  | 0.957734  |

#### 3.2.5 CatBoost  
CatBoost is specifically designed to handle categorical features efficiently without extensive preprocessing. It reduces overfitting through ordered boosting and provides robust performance on imbalanced datasets. CatBoost's ability to handle categorical data natively makes it ideal for datasets with mixed feature types, improving classification accuracy without requiring complex feature engineering.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/CVCV.png?raw=tr)
Best Learning Rate: 0.1
|            | Precision | Recall    | F1-Score  |
|------------|-----------|-----------|-----------|
| 0          | 0.967536  | 0.972799  | 0.970160  |
| 1          | 0.972678  | 0.967391  | 0.970027  |
| Accuracy   | 0.970107  |
| Macro Avg  | 0.970107  | 0.970095  | 0.970094  |

#### 3.2.6 XGBoost 
XGBoost is an optimized distributed gradient boosting library that focuses on performance and speed. It builds decision trees sequentially with an emphasis on handling sparse data and missing values efficiently. XGBoost excels in scenarios requiring fast training and prediction times while maintaining high accuracy, making it suitable for real-time phishing detection applications.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/XGBCV.png?raw=tr)
Best Learning Rate: 0.8
|            | Precision | Recall    | F1-Score  |
|------------|-----------|-----------|-----------|
| 0          | 0.967838  | 0.967359  | 0.967598  |
| 1          | 0.967407  | 0.967885  | 0.967646  |
| Accuracy   | 0.967622  |  |
| Macro Avg  | 0.967623  | 0.967622  | 0.967622  |


### 3.3 Develop Browser Extension  
Based on the results shown in the table, I built a Chrome extension to deploy the best-performing model using Flask as the backend. The extension automatically captures the current page being visited and, upon clicking a button, sends a request to the Flask server to obtain prediction results.
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/IMPL.png?raw=true)
  
## 4. Experimental results  
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/RES.png?raw=true)
- **Best Overall Performance**: **Random Forest**
  - It has the highest accuracy (0.971) and F1-score (0.972).
  - Very high recall (0.991) and precision (0.994), indicating strong performance in both detecting true positives and minimizing false positives.
  - Fast prediction time (0.010 seconds), making it efficient for real-time applications.

- **Fastest Model**: **Decision Tree**
  - Although its accuracy is lower, it has the fastest prediction time (0.001 seconds).

- **Other Considerations**:
  - **CatBoost Classifier** offers a good balance with high accuracy and very low prediction time.
  - **K-Nearest Neighbors** has excellent recall and precision but is much slower in prediction.

Overall, **Random Forest** stands out as the best-performing model due to its high accuracy, balanced metrics, and efficient prediction time, making it suitable for applications requiring both accuracy and speed.

### Important Features
![enter image description here](https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning/blob/master/Image/Top20.png?raw=true)
  
## 5. Future work  

1. **Feature Enhancement**:
   - Explore additional features that can improve model accuracy and robustness, such as user interaction patterns and advanced content analysis.

2. **Model Optimization**:
   - Experiment with hyperparameter tuning and ensemble methods to further enhance model performance and reduce false positives.

3. **Real-Time Deployment**:
   - Implement the model in real-time systems, optimizing for speed and scalability to handle large volumes of web traffic efficiently.

4. **Cross-Platform Extensions**:
   - Develop browser extensions for multiple platforms (e.g., Firefox, Safari) to broaden the application’s reach.

5. **Adaptive Learning**:
   - Incorporate adaptive learning techniques to continuously update the model with new phishing strategies, ensuring it remains effective against evolving threats.

6. **User Interface Improvements**:
   - Enhance the user interface of the browser extension for better usability and user experience, making it more intuitive for non-technical users. 
  
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