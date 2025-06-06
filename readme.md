# EasyBill - Smart Invoicing for Small Business

EasyBill is a modern, web-based invoicing application built with Django that helps small businesses and freelancers create professional invoices, track payments, and manage their finances efficiently.

## Features

### 📊 Dashboard & Analytics
- Real-time business insights and financial overview
- Interactive charts showing revenue trends and invoice status distribution
- Key metrics tracking (total revenue, pending payments, client count)
- Recent activity monitoring

### 📄 Invoice Management
- Create and edit professional invoices in under 60 seconds
- Automatic invoice numbering and calculations
- Support for discounts and VAT
- Multiple invoice statuses (Created, Pending, Paid)
- Invoice list view with filtering capabilities

### 👥 Client Management
- Comprehensive client database
- Client contact information storage
- Individual client detail pages
- Invoice history per client

### 🎨 Modern UI/UX
- Dark theme with gradient accents
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Glass-morphism design elements

## Technology Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite (default), PostgreSQL support via dj-database-url
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS, Custom CSS
- **Charts**: Chart.js for data visualization

## Project Structure

```
Bill/
├── Bill/                   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── EasyBill/              # Main application
│   ├── models.py          # Data models (Invoice, Client, etc.)
│   ├── views.py           # View controllers
│   ├── urls.py            # URL routing
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── dashboard.html     # Main dashboard
│   ├── invoice_create.html # Invoice creation form
│   ├── clients.html       # Client listing
│   ├── login.html         # Authentication
│   └── register.html      # User registration
├── static/               # Static assets
│   ├── styles.css        # Custom CSS
│   └── rb_36.png         # Logo and images
└── requirements.txt      # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bill
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## Configuration

### Environment Variables
The application supports environment-based configuration. Key settings include:

- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Debug mode (set to False in production)
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

### Database Configuration
The project uses SQLite by default but supports PostgreSQL through the `dj-database-url` package. To use PostgreSQL, set the `DATABASE_URL` environment variable.

## Usage

### Getting Started
1. Register a new account or login
2. Add your first client from the Clients page
3. Create your first invoice using the "New Invoice" button
4. Track your business performance on the Dashboard

### Creating Invoices
1. Navigate to the Dashboard and click "New Invoice"
2. Select a client from the dropdown
3. Add invoice line items (description, quantity, rate)
4. Apply discounts and VAT if needed
5. Save the invoice

### Managing Clients
1. Go to the Clients page
2. Click "Register New Client" to add clients
3. Fill in client details (name, email, phone, address)
4. View client details and invoice history

## Key Models

### Client
- Name, email, phone, address
- One-to-many relationship with invoices

### Invoice
- Client reference
- Invoice number (auto-generated)
- Status (created, pending, paid)
- Total amount calculation
- Creation and due dates

### InvoiceLine
- Description, quantity, rate
- Belongs to an invoice
- Automatic line total calculation

## API Endpoints

The application includes several key views:
- `/` - Landing page
- `/dashboard/` - Main dashboard
- `/invoices/` - Invoice management
- `/clients/` - Client management
- `/overview/` - Business analytics
- `/login/` - Authentication
- `/register/` - User registration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

## Future Enhancements

- [ ] PDF invoice generation
- [ ] Email invoice sending
- [ ] Payment gateway integration
- [ ] Multi-currency support
- [ ] Recurring invoices
- [ ] Advanced reporting
- [ ] API endpoints for mobile app integration
