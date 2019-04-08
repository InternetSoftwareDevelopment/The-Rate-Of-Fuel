from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import Quote, RegistrationForm, LoginForm, UpdateAccountForm
from app.models import Client, Quotes
from flask_login import login_user, current_user, logout_user, login_required

# Home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.create_all()
        client = Client(username=form.username.data, name=form.name.data, address=form.address.data,
                        city=form.city.data, state=form.state.data, zip=form.zip.data, phone=form.phone.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(client)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(email=form.email.data).first()
        if client and bcrypt.check_password_hash(client.password, form.password.data):
            login_user(client, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# account route
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

# Request a Quote page
@app.route("/requestAQuote", methods=['GET', 'POST'])
@login_required
def requestAQuote():
    form = Quote()
    if form.validate_on_submit():
        db.create_all()
        quote = Quotes(client_id=current_user.clientID, gallonsRequested=form.gallons_requested.data,
                    requestDate=form.request_date.data, deliveryDate=form.delivery_date.data,
                    address=form.delivery_address.data, city=form.delivery_city.data, state=form.delivery_state.data,
                    zip=form.delivery_zip.data, name=form.delivery_contact_name.data, phone=form.delivery_contact_phone.data,
                    email=form.delivery_contact_email.data, suggestedPrice=form.suggested_price.data,
                    totalAmountDue=form.total_amount_due.data)
        db.session.add(quote)
        db.session.commit()
        flash(f'Submission Sucessful. Thank You {form.delivery_contact_name.data}! Someone will get back with you.','success')
        return redirect(url_for('home'))

    return render_template('requestAQuote.html', title='Request a Quote', form=form)


# client Information page
@app.route('/ClientInformation')
def ClientInformation():
    form = ClientInformation()
    return render_template('ClientInformation.html', form=form)


# Quote History page
@app.route('/QuoteHistory')
@login_required
def QuoteHistory():
    quotes = Quotes.query.all()
    return render_template('QuoteHistory.html', quotes=quotes)