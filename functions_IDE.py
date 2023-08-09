import requests
import pandas as pd
import json


def get_api(base_url="https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws",end_point="/mentorskool/v1/sales?offset=0&limit=100",headers={"access_token":"fe66583bfe5185048c66571293e0d358"}):
    """
    This function loops through the api to fetch all the records and return it in a list.This function takes all types of errors into account.
    :param base_url:Base url of the api
           endpoint:endpoint for fetching the record from that page
           headers: contains the access token for authorization
    :return: A list conatining all the data
    """
    final_list=[]
    for i in range(5):
        try:

            response = requests.get(base_url+end_point,headers=headers)

            response_data = response.json()
            data=response_data['data']
            final_list.extend(data)
            end_point= response_data['next']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTPError:",{http_err})
        except Exception as err:
            print(f"Error:", {err})
    return final_list


whole_list = get_api()

sales_df = pd.json_normalize(whole_list)

sales_df.dtypes


sales_df.replace('null',None,inplace=True)
sales_df.isnull().sum()


sales_df['order.order_purchase_date']=pd.to_datetime(sales_df['order.order_purchase_date'])
sales_df['order.order_approved_at']=pd.to_datetime(sales_df['order.order_approved_at'])
sales_df['order.order_delivered_carrier_date']=pd.to_datetime(sales_df['order.order_delivered_carrier_date'])
sales_df['order.order_delivered_customer_date']=pd.to_datetime(sales_df['order.order_delivered_customer_date'])
sales_df['order.order_estimated_delivery_date']=pd.to_datetime(sales_df['order.order_estimated_delivery_date'])

def product_size(df,product):
    product_sizes= df[df['product.product_name']==product]['product.sizes'].unique()
    return product_sizes


a = product_size(sales_df,'Mitel 5320 IP Phone VoIP phone')
print(a)


# which month had the highest sales overall?
sales_df['month'] = sales_df['order.order_purchase_date'].apply(lambda date:date.strftime('%B'))

monthly_sales=sales_df.groupby('month')['sales_amt'].sum()
print('highest sale by month:',monthly_sales.idxmax())

# which month had the highest overall profit?

monthly_profit = sales_df.groupby('month')['profit_amt'].sum()
print('highest profit by month:',monthly_profit.sort_values(ascending=False).index[0])


# how many months have lead to a positive profit margin?

num_positive_months=(monthly_profit>0).sum()
print('No. of months with positive monthly profit:',num_positive_months)

sales_df['delay']=  (sales_df['order.order_delivered_customer_date']-sales_df['order.order_estimated_delivery_date']).dt.days

sales_df['delay_status'] = sales_df['delay'].apply(lambda x: 'Late' if x>0 else('Early' if x<0 else 'On Time'))

# how many orders are late delivered to the customers?

late_order_count=(sales_df['delay_status']=='Late').sum()
print('total late orders:', late_order_count)

# which vendor has the highest late deliveries?

late_df = sales_df[sales_df['delay_status']=='Late']
vendor_late_delivery_count = late_df.groupby('order.vendor.VendorID')['id'].count()
print('vendor with most late deliveries:',vendor_late_delivery_count.idxmax())


sales_df[['first_name','last_name']] = sales_df['order.customer.customer_name'].str.split(' ',n=1,expand=True)

# how many customers have a first name like Alan?
count_firstname = sum(1 for name in sales_df['first_name'] if name=='Alan')
print('number of entries with firstname Alan:', count_firstname)


