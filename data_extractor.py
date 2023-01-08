import ijson
import csv

csv_file = open('hirability_balanced.csv', 'w', encoding='UTF8')
csv_writer = csv.writer(csv_file)

top_countries = ['India', 'Ukraine', 'China', 'Poland', 'Philippines']
countries = {}

with open('data.json', 'rb') as f:
    data_count = 0
    iteration = 0
    for record in ijson.items(f, '', multiple_values=True):
        if data_count == 500:
            break
        if record['location'] and record['location'].title() in top_countries:
            if record['location'].title() not in countries:
                countries[record['location'].title()] = {
                    'hireable': 0,
                    'not_hireable': 0
                }
            if record['location'].title() in countries and \
                    ((record['hirable'] and countries[record['location'].title()]['hireable'] < 250) or
                        ((not record['hirable']) and countries[record['location'].title()]['not_hireable'] < 250)) and \
                    data_count < 2500:

                email = 1 if record['email'] and record['email'] != 'null' else 0
                company = 1 if record['company'] and record['company'] != 'null' else 0
                suspicious = 1 if record['is_suspicious'] else 0
                location = record['location'].title()
                has_bio = 1 if record['bio'] else 0
                has_blog = 1 if record['blog'] else 0
                followers = record['followers']
                followings = record['following']
                commits = record['commits']
                public_gists = record['public_gists']
                public_repos = len(record['repo_list']) if record['repo_list'] else 0
                hirable = 1 if record['hirable'] else 0

                if hirable:
                    countries[record['location'].title()]['hireable'] += 1
                else:
                    countries[record['location'].title()]['not_hireable'] += 1

                data = [
                    email,
                    company,
                    suspicious,
                    location,
                    has_bio,
                    has_blog,
                    followers,
                    followings,
                    commits,
                    public_gists,
                    public_repos,
                    hirable
                ]
                try:
                    csv_writer.writerow(data)
                    print('new data written')
                except UnicodeEncodeError:
                    print('writing failed. Error detected')
                data_count += 1

csv_file.close()
