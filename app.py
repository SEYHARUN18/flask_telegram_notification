from flask import Flask, render_template, request, redirect
import requests
from datetime import date

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    res = requests.get('https://fakestoreapi.com/products')
    res_json = res.json()
    return render_template('home.html', product_list=res_json)


@app.route('/shop_now')
def shop_now():
    id = request.args.get('id')
    res = requests.get(f'https://fakestoreapi.com/products/{id}')
    json = res.json()
    return render_template('shop_now.html', product=json)


@app.route('/check_out')
def check_out():
    id = request.args.get('id')
    res = requests.get(f'https://fakestoreapi.com/products/{id}')
    json = res.json()
    return render_template('check_out.html', product=json)


@app.post('/submit_checkout')
def submit_checkout():
    id = request.form.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{id}")
    product = res.json()

    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    quantity = request.form.get('quantity')

    if quantity is None or quantity == '':
        quantity = 1
    else:
        quantity = int(quantity)

    total_price = product['price'] * quantity

    msg = (
        "<b>🔔 New Confirm Booking 🔔</b>\n"
        "<code> - Name: {name}</code>\n"
        "<code> - Phone: {phone}</code>\n"
        "<code> - Email: {email}</code>\n"
        "<code> - Address: {address}</code>\n"
        "<code> - Date: {date}</code>\n"
        "<code>================================</code>\n"
        "<b>🔔 Order Detail 🔔</b>\n"
        "<code>1. {product_name} {quantity}x{price} = ${total_price}</code>\n"
    ).format(
        name=name,
        phone=phone,
        email=email,
        address=address,
        date=date.today(),
        product_name=product['title'],
        quantity=quantity,
        price=product['price'],
        total_price=total_price
    )

    notify_res = send_notification(msg)
    return redirect('/thank_you')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


def send_notification(msg):
    bot_token = '6971179618:AAGCaFEWzQiE5T2Cr88vBBN1VjZ3uaqfdLY'
    chat_id = '@botpythonss25'

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={requests.utils.quote(msg)}&parse_mode=HTML"
    res = requests.get(url)
    return res


if __name__ == '__main__':
    app.run(debug=True)
