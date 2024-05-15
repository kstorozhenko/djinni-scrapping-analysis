import csv
import requests
from bs4 import BeautifulSoup
from models import Vacancy
from config import regex_pattern
import re


class Scraper:
    def __init__(self):
        self.url = "https://djinni.co/jobs/?primary_keyword=Python"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_page_content(self, page_number=1):
        response = requests.get(f"{self.url}&page={page_number}", headers=self.headers)
        return BeautifulSoup(response.text, "html.parser")

    def extract_vacancies(self, soup):
        vacancies = []
        for vacancy_li in soup.find_all("li", class_="list-jobs__item job-list__item"):
            title = vacancy_li.find("a", class_="h3 job-list-item__link").text.strip()
            company = vacancy_li.find("a", class_="mr-2").text.strip()
            location = vacancy_li.find("span", class_="location-text").text.strip()
            description_element = vacancy_li.find(
                "div", class_="job-list-item__description"
            )
            description_text = description_element.text
            requirements = re.findall(regex_pattern, description_text, re.IGNORECASE)
            views_count = int(
                vacancy_li.find("span", class_="bi bi-eye").parent.text.strip()
            )
            reviews_count = int(
                vacancy_li.find("span", class_="bi bi-people").parent.text.strip()
            )
            vacancies.append(
                Vacancy(
                    title, company, location, requirements, views_count, reviews_count
                )
            )
        return vacancies

    def save_to_csv(self, vacancies):
        with open("../analysis/vacancies.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Title",
                    "Company",
                    "Location",
                    "Requirements",
                    "Views Count",
                    "Reviews Count",
                ]
            )
            for vacancy in vacancies:
                writer.writerow(
                    [
                        vacancy.title,
                        vacancy.company,
                        vacancy.location,
                        ", ".join(vacancy.requirements),
                        vacancy.views_count,
                        vacancy.reviews_count,
                    ]
                )

    def scrape(self):
        page_number = 1
        all_vacancies = []
        while True:
            soup = self.get_page_content(page_number)
            vacancies = self.extract_vacancies(soup)
            if not vacancies:
                break
            all_vacancies.extend(vacancies)
            page_number += 1
        self.save_to_csv(all_vacancies)
        return all_vacancies


if __name__ == "__main__":
    scraper = Scraper()
    vacancies = scraper.scrape()
    for vacancy in vacancies:
        print(vacancy)
