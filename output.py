import pandas as pd

class AmazonSalesReport:
    def __init__(self, csv_file):
        """
        Initialize6 the AmazonSalesReport class with the provided CSV file.
        """
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
    
    def generate_state_orders(self):
        """
        Generate a report of total number of sales with regards to ship-state.
        """
        state_orders = self.df.groupby('ship-state').size().reset_index(name='Total Sales')
        return state_orders
    
    def generate_category_orders(self):
        """
        Generate a report of total number of sales with regards to category.
        """
        category_orders = self.df.groupby('Category').size().reset_index(name='Total Sales')
        return category_orders
    
    def generate_top_20_products(self):
        """
        Generate a report of top 20 selling products and total units sold.
        """
        top_20_products = self.df.groupby('ASIN')['Qty'].sum().reset_index().sort_values(by='Qty', ascending=False).head(20)
        return top_20_products
    
    def save_to_excel(self, output_file):
        """
        Save the reports to an Excel file with multiple sheets.
        """
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generate_state_orders().to_excel(writer, sheet_name='State Orders', index=False)
            self.generate_category_orders().to_excel(writer, sheet_name='Category Orders', index=False)
            self.generate_top_20_products().to_excel(writer, sheet_name='Top 20 Products', index=False)
        print(f'Reports have been saved to {output_file}')
    
if __name__ == "__main__":
    # Example usage
    csv_file = 'Amazon Sale Report.csv'
    output_file = 'Amazon_Sale_Report.xlsx'
    
    report = AmazonSalesReport(csv_file)
    report.save_to_excel(output_file)
