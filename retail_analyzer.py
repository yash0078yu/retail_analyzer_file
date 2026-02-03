import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from datetime import datetime
import sys

class RetailAnalyzer:

    def _init_(self):
        self.data = None
        self.filtered_data = None

    def load_data(self, file_path):
        if not file_path.endswith(".csv"):
            print("Invalid file format")
            sys.exit()

        try:
            self.data = pd.read_csv(file_path)

            required_columns = [
                "Date",
                "Product",
                "Category",
                "Price",
                "Quantity Sold",
                "Total Sales"
            ]

            for col in required_columns:
                if col not in self.data.columns:
                    print("Missing column:", col)
                    sys.exit()

            self.data["Date"] = pd.to_datetime(self.data["Date"])

            print("Data loaded successfully")

        except Exception as e:
            print("Error:", e)
            sys.exit()

    def clean_data(self):
        if self.data is None:
            print("No data to clean")
            return

        self.data.fillna(0, inplace=True)

        for i in range(len(self.data)):
            if self.data.loc[i, "Price"] < 0:
                self.data.loc[i, "Price"] = 0
            if self.data.loc[i, "Quantity Sold"] < 0:
                self.data.loc[i, "Quantity Sold"] = 0

        self.data["Total Sales"] = self.data["Price"] * self.data["Quantity Sold"]

        print("Data cleaned")

    def calculate_metrics(self):
        if self.data is None:
            print("No data loaded")
            return

        total_sales = np.sum(self.data["Total Sales"])
        average_sales = np.mean(self.data["Total Sales"])
        max_sales = np.max(self.data["Total Sales"])
        min_sales = np.min(self.data["Total Sales"])

        product_sales = self.data.groupby("Product")["Quantity Sold"].sum()
        popular_product = product_sales.idxmax()

        print("\nMetrics")
        print("Total Sales:", total_sales)
        print("Average Sales:", average_sales)
        print("Maximum Sale:", max_sales)
        print("Minimum Sale:", min_sales)
        print("Most Popular Product:", popular_product)

    def category_analysis(self):
        category_data = self.data.groupby("Category")["Total Sales"].sum()
        print("\nCategory Wise Sales")
        print(category_data)

    def date_analysis(self):
        date_data = self.data.groupby("Date")["Total Sales"].sum()
        print("\nDate Wise Sales")
        print(date_data)

    def filter_data(self, category=None, start_date=None, end_date=None):
        filtered = self.data

        if category:
            filtered = filtered[filtered["Category"] == category]

        if start_date and end_date:
            filtered = filtered[
                (filtered["Date"] >= start_date) &
                (filtered["Date"] <= end_date)
            ]

        self.filtered_data = filtered
        return filtered

    def display_summary(self):
        if self.data is None:
            print("No data loaded")
            return

        print("\nSummary")
        print(self.data.describe(include="all"))

    def visualize_category_sales(self):
        category_sales = self.data.groupby("Category")["Total Sales"].sum()
        category_sales.plot(kind="bar")
        plt.title("Total Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.show()

    def visualize_sales_trend(self):
        trend = self.data.groupby("Date")["Total Sales"].sum()
        plt.plot(trend.index, trend.values)
        plt.title("Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.show()

    def visualize_heatmap(self):
        corr = self.data[["Price", "Quantity Sold", "Total Sales"]].corr()
        sns.heatmap(corr, annot=True)
        plt.title("Correlation Heatmap")
        plt.show()

    def visualize_all(self):
        self.visualize_category_sales()
        self.visualize_sales_trend()
        self.visualize_heatmap()


def main():
    analyzer = RetailAnalyzer()

    file_path = input("Enter CSV file path: ")
    analyzer.load_data(file_path)
    analyzer.clean_data()

    while True:
        print("\nMenu")
        print("1. Calculate Metrics")
        print("2. Category Analysis")
        print("3. Date Analysis")
        print("4. Filter Data")
        print("5. Display Summary")
        print("6. Visualize Data")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            analyzer.calculate_metrics()

        elif choice == "2":
            analyzer.category_analysis()

        elif choice == "3":
            analyzer.date_analysis()

        elif choice == "4":
            category = input("Enter category or press Enter: ")
            start = input("Start date YYYY-MM-DD or press Enter: ")
            end = input("End date YYYY-MM-DD or press Enter: ")

            if start and end:
                start = datetime.strptime(start, "%Y-%m-%d")
                end = datetime.strptime(end, "%Y-%m-%d")
            else:
                start = end = None

            result = analyzer.filter_data(category or None, start, end)
            print(result)

        elif choice == "5":
            analyzer.display_summary()

        elif choice == "6":
            analyzer.visualize_all()

        elif choice == "7":
            print("Program Ended")
            break

        else:
            print("Invalid choice")

main()