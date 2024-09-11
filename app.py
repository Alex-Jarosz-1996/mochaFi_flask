import os

from flask import Flask, jsonify, request

# from backend import get_yf_stock_data
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from backend.common.core import get_yf_stock_data
from backend.data.utils.controller import StockController

# initialising flask app
app = Flask(__name__)
CORS(app=app)

# Configuring db
db_path = os.path.join(os.path.dirname(__file__), "app.db")
db_uri = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Deleting the db before it is created
if os.path.exists(db_path):
    os.remove(db_path)

db = SQLAlchemy(app)


class StockModel(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    country = db.Column(db.String(5), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=True)
    marketCap = db.Column(db.Float, nullable=True)
    numSharesAvail = db.Column(db.Float, nullable=True)
    yearlyLowPrice = db.Column(db.Float, nullable=True)
    yearlyHighPrice = db.Column(db.Float, nullable=True)
    fiftyDayMA = db.Column(db.Float, nullable=True)
    twoHundredDayMA = db.Column(db.Float, nullable=True)
    acquirersMultiple = db.Column(db.Float, nullable=True)
    currentRatio = db.Column(db.Float, nullable=True)
    enterpriseValue = db.Column(db.Float, nullable=True)
    eps = db.Column(db.Float, nullable=True)
    evToEBITDA = db.Column(db.Float, nullable=True)
    evToRev = db.Column(db.Float, nullable=True)
    peRatioTrail = db.Column(db.Float, nullable=True)
    peRatioForward = db.Column(db.Float, nullable=True)
    priceToSales = db.Column(db.Float, nullable=True)
    priceToBook = db.Column(db.Float, nullable=True)
    dividendYield = db.Column(db.Float, nullable=True)
    dividendRate = db.Column(db.Float, nullable=True)
    exDivDate = db.Column(db.String, nullable=True)
    payoutRatio = db.Column(db.Float, nullable=True)
    bookValPerShare = db.Column(db.Float, nullable=True)
    cash = db.Column(db.Float, nullable=True)
    cashPerShare = db.Column(db.Float, nullable=True)
    cashToMarketCap = db.Column(db.Float, nullable=True)
    cashToDebt = db.Column(db.Float, nullable=True)
    debt = db.Column(db.Float, nullable=True)
    debtToMarketCap = db.Column(db.Float, nullable=True)
    debtToEquityRatio = db.Column(db.Float, nullable=True)
    returnOnAssets = db.Column(db.Float, nullable=True)
    returnOnEquity = db.Column(db.Float, nullable=True)
    ebitda = db.Column(db.Float, nullable=True)
    ebitdaPerShare = db.Column(db.Float, nullable=True)
    earningsGrowth = db.Column(db.Float, nullable=True)
    grossProfit = db.Column(db.Float, nullable=True)
    grossProfitPerShare = db.Column(db.Float, nullable=True)
    netIncome = db.Column(db.Float, nullable=True)
    netIncomePerShare = db.Column(db.Float, nullable=True)
    operatingMargin = db.Column(db.Float, nullable=True)
    profitMargin = db.Column(db.Float, nullable=True)
    revenue = db.Column(db.Float, nullable=True)
    revenueGrowth = db.Column(db.Float, nullable=True)
    revenuePerShare = db.Column(db.Float, nullable=True)
    fcf = db.Column(db.Float, nullable=True)
    fcfToMarketCap = db.Column(db.Float, nullable=True)
    fcfPerShare = db.Column(db.Float, nullable=True)
    fcfToEV = db.Column(db.Float, nullable=True)
    ocf = db.Column(db.Float, nullable=True)
    ocfToRevenueRatio = db.Column(db.Float, nullable=True)
    ocfToMarketCap = db.Column(db.Float, nullable=True)
    ocfPerShare = db.Column(db.Float, nullable=True)
    ocfToEV = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Stock {self.code}>"


# TODO: ADD
# class FinancialData(db.Model):
#     __tablename__ = 'financial_data'
#     id = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.Integer, db.ForeignKey('stock.code'), nullable=False)


# TODO: ADD
# class StockChart(db.Model):
#     __tablename__ = "stock_chart"


# TODO: ADD
# class BackTest(db.Model):
#     __tablename__ = "back_test"


# TODO: ADD
# class TradeBot(db.Model):
#     __tablename__ = "trade_bot"

# Create the database tables
with app.app_context():
    db.create_all()

# API route to handle stock selection and save to database
@app.route('/stock', methods=['POST'])
def add_stock():
    data = request.json
    code = data.get('stock')
    country = data.get('country')

    print(f"Received request to add stock: {code} from {country}")

    existing_stock = StockModel.query.filter_by(code=code, country=country).first()
    if existing_stock:
        return jsonify({"error": "Stock already exists"}), 409

    stock_obj = StockController(code, country)
    
    try:
        new_stock = StockModel(
            code=stock_obj.si.ticker,
            country=stock_obj.si.country,
            price=getattr(stock_obj.si.stockPriceMetrics, 'price', None),
            marketCap=getattr(stock_obj.si.stockPriceMetrics, 'marketCap', None),
            numSharesAvail=getattr(stock_obj.si.stockPriceMetrics, 'numSharesAvail', None),
            yearlyLowPrice=getattr(stock_obj.si.stockPriceMetrics, 'yearlyLowPrice', None),
            yearlyHighPrice=getattr(stock_obj.si.stockPriceMetrics, 'yearlyHighPrice', None),
            fiftyDayMA=getattr(stock_obj.si.stockPriceMetrics, 'fiftyDayMA', None),
            twoHundredDayMA=getattr(stock_obj.si.stockPriceMetrics, 'twoHundredDayMA', None),
            acquirersMultiple=getattr(stock_obj.si.valueMetrics, 'acquirersMultiple', None),
            currentRatio=getattr(stock_obj.si.valueMetrics, 'currentRatio', None),
            enterpriseValue=getattr(stock_obj.si.valueMetrics, 'enterpriseValue', None),
            eps=getattr(stock_obj.si.valueMetrics, 'eps', None),
            evToEBITDA=getattr(stock_obj.si.valueMetrics, 'evToEBITDA', None),
            evToRev=getattr(stock_obj.si.valueMetrics, 'evToRev', None),
            peRatioTrail=getattr(stock_obj.si.valueMetrics, 'peRatioTrail', None),
            peRatioForward=getattr(stock_obj.si.valueMetrics, 'peRatioForward', None),
            priceToSales=getattr(stock_obj.si.valueMetrics, 'priceToSales', None),
            priceToBook=getattr(stock_obj.si.valueMetrics, 'priceToBook', None),
            dividendYield=getattr(stock_obj.si.dividendMetrics, 'dividendYield', None),
            dividendRate=getattr(stock_obj.si.dividendMetrics, 'dividendRate', None),
            exDivDate=getattr(stock_obj.si.dividendMetrics, 'exDivDate', None),
            payoutRatio=getattr(stock_obj.si.dividendMetrics, 'payoutRatio', None),
            bookValPerShare=getattr(stock_obj.si.balanceSheetMetrics, 'bookValPerShare', None),
            cash=getattr(stock_obj.si.balanceSheetMetrics, 'cash', None),
            cashPerShare=getattr(stock_obj.si.balanceSheetMetrics, 'cashPerShare', None),
            cashToMarketCap=getattr(stock_obj.si.balanceSheetMetrics, 'cashToMarketCap', None),
            cashToDebt=getattr(stock_obj.si.balanceSheetMetrics, 'cashToDebt', None),
            debt=getattr(stock_obj.si.balanceSheetMetrics, 'debt', None),
            debtToMarketCap=getattr(stock_obj.si.balanceSheetMetrics, 'debtToMarketCap', None),
            debtToEquityRatio=getattr(stock_obj.si.balanceSheetMetrics, 'debtToEquityRatio', None),
            returnOnAssets=getattr(stock_obj.si.balanceSheetMetrics, 'returnOnAssets', None),
            returnOnEquity=getattr(stock_obj.si.balanceSheetMetrics, 'returnOnEquity', None),
            ebitda=getattr(stock_obj.si.incomeRelatedMetrics, 'ebitda', None),
            ebitdaPerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'ebitdaPerShare', None),
            earningsGrowth=getattr(stock_obj.si.incomeRelatedMetrics, 'earningsGrowth', None),
            grossProfit=getattr(stock_obj.si.incomeRelatedMetrics, 'grossProfit', None),
            grossProfitPerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'grossProfitPerShare', None),
            netIncome=getattr(stock_obj.si.incomeRelatedMetrics, 'netIncome', None),
            netIncomePerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'netIncomePerShare', None),
            operatingMargin=getattr(stock_obj.si.incomeRelatedMetrics, 'operatingMargin', None),
            profitMargin=getattr(stock_obj.si.incomeRelatedMetrics, 'profitMargin', None),
            revenue=getattr(stock_obj.si.incomeRelatedMetrics, 'revenue', None),
            revenueGrowth=getattr(stock_obj.si.incomeRelatedMetrics, 'revenueGrowth', None),
            revenuePerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'revenuePerShare', None),
            fcf=getattr(stock_obj.si.cashFlowMetrics, 'fcf', None),
            fcfToMarketCap=getattr(stock_obj.si.cashFlowMetrics, 'fcfToMarketCap', None),
            fcfPerShare=getattr(stock_obj.si.cashFlowMetrics, 'fcfPerShare', None),
            fcfToEV=getattr(stock_obj.si.cashFlowMetrics, 'fcfToEV', None),
            ocf=getattr(stock_obj.si.cashFlowMetrics, 'ocf', None),
            ocfToRevenueRatio=getattr(stock_obj.si.cashFlowMetrics, 'ocfToRevenueRatio', None),
            ocfToMarketCap=getattr(stock_obj.si.cashFlowMetrics, 'ocfToMarketCap', None),
            ocfPerShare=getattr(stock_obj.si.cashFlowMetrics, 'ocfPerShare', None),
            ocfToEV=getattr(stock_obj.si.cashFlowMetrics, 'ocfToEV', None)
        )
        db.session.add(new_stock)
        db.session.commit()
    except AttributeError as e:
        print(f"Error fetching data for {code}: {e}")
        return jsonify({"error": "Error fetching stock data"}), 500

    return jsonify({
        "message": "Stock added successfully",
        "code": new_stock.code,
        "country": new_stock.country,
        "price": new_stock.price,
        "marketCap": new_stock.marketCap,
        "numSharesAvail": new_stock.numSharesAvail,
        "yearlyLowPrice": new_stock.yearlyLowPrice,
        "yearlyHighPrice": new_stock.yearlyHighPrice,
        "fiftyDayMA": new_stock.fiftyDayMA,
        "twoHundredDayMA": new_stock.twoHundredDayMA,
        "acquirersMultiple": new_stock.acquirersMultiple,
        "currentRatio": new_stock.currentRatio,
        "enterpriseValue": new_stock.enterpriseValue,
        "eps": new_stock.eps,
        "evToEBITDA": new_stock.evToEBITDA,
        "evToRev": new_stock.evToRev,
        "peRatioTrail": new_stock.peRatioTrail,
        "peRatioForward": new_stock.peRatioForward,
        "priceToSales": new_stock.priceToSales,
        "priceToBook": new_stock.priceToBook,
        "dividendYield": new_stock.dividendYield,
        "dividendRate": new_stock.dividendRate,
        "exDivDate": new_stock.exDivDate,
        "payoutRatio": new_stock.payoutRatio,
        "bookValPerShare": new_stock.bookValPerShare,
        "cash": new_stock.cash,
        "cashPerShare": new_stock.cashPerShare,
        "cashToMarketCap": new_stock.cashToMarketCap,
        "cashToDebt": new_stock.cashToDebt,
        "debt": new_stock.debt,
        "debtToMarketCap": new_stock.debtToMarketCap,
        "debtToEquityRatio": new_stock.debtToEquityRatio,
        "returnOnAssets": new_stock.returnOnAssets,
        "returnOnEquity": new_stock.returnOnEquity,
        "ebitda": new_stock.ebitda,
        "ebitdaPerShare": new_stock.ebitdaPerShare,
        "earningsGrowth": new_stock.earningsGrowth,
        "grossProfit": new_stock.grossProfit,
        "grossProfitPerShare": new_stock.grossProfitPerShare,
        "netIncome": new_stock.netIncome,
        "netIncomePerShare": new_stock.netIncomePerShare,
        "operatingMargin": new_stock.operatingMargin,
        "profitMargin": new_stock.profitMargin,
        "revenue": new_stock.revenue,
        "revenueGrowth": new_stock.revenueGrowth,
        "revenuePerShare": new_stock.revenuePerShare,
        "fcf": new_stock.fcf,
        "fcfToMarketCap": new_stock.fcfToMarketCap,
        "fcfPerShare": new_stock.fcfPerShare,
        "fcfToEV": new_stock.fcfToEV,
        "ocf": new_stock.ocf,
        "ocfToRevenueRatio": new_stock.ocfToRevenueRatio,
        "ocfToMarketCap": new_stock.ocfToMarketCap,
        "ocfPerShare": new_stock.ocfPerShare,
        "ocfToEV": new_stock.ocfToEV
    }), 201


@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = StockModel.query.all()
    return jsonify([{
        "id": stock.id, 
        "code": stock.code,
        "country": stock.country,
        "price": stock.price,
        "marketCap": stock.marketCap,
        "numSharesAvail": stock.numSharesAvail,
        "yearlyLowPrice": stock.yearlyLowPrice,
        "yearlyHighPrice": stock.yearlyHighPrice,
        "fiftyDayMA": stock.fiftyDayMA,
        "twoHundredDayMA": stock.twoHundredDayMA,
        "acquirersMultiple": stock.acquirersMultiple,
        "currentRatio": stock.currentRatio,
        "enterpriseValue": stock.enterpriseValue,
        "eps": stock.eps,
        "evToEBITDA": stock.evToEBITDA,
        "evToRev": stock.evToRev,
        "peRatioTrail": stock.peRatioTrail,
        "peRatioForward": stock.peRatioForward,
        "priceToSales": stock.priceToSales,
        "priceToBook": stock.priceToBook,
        "dividendYield": stock.dividendYield,
        "dividendRate": stock.dividendRate,
        "exDivDate": stock.exDivDate,
        "payoutRatio": stock.payoutRatio,
        "bookValPerShare": stock.bookValPerShare,
        "cash": stock.cash,
        "cashPerShare": stock.cashPerShare,
        "cashToMarketCap": stock.cashToMarketCap,
        "cashToDebt": stock.cashToDebt,
        "debt": stock.debt,
        "debtToMarketCap": stock.debtToMarketCap,
        "debtToEquityRatio": stock.debtToEquityRatio,
        "returnOnAssets": stock.returnOnAssets,
        "returnOnEquity": stock.returnOnEquity,
        "ebitda": stock.ebitda,
        "ebitdaPerShare": stock.ebitdaPerShare,
        "earningsGrowth": stock.earningsGrowth,
        "grossProfit": stock.grossProfit,
        "grossProfitPerShare": stock.grossProfitPerShare,
        "netIncome": stock.netIncome,
        "netIncomePerShare": stock.netIncomePerShare,
        "operatingMargin": stock.operatingMargin,
        "profitMargin": stock.profitMargin,
        "revenue": stock.revenue,
        "revenueGrowth": stock.revenueGrowth,
        "revenuePerShare": stock.revenuePerShare,
        "fcf": stock.fcf,
        "fcfToMarketCap": stock.fcfToMarketCap,
        "fcfPerShare": stock.fcfPerShare,
        "fcfToEV": stock.fcfToEV,
        "ocf": stock.ocf,
        "ocfToRevenueRatio": stock.ocfToRevenueRatio,
        "ocfToMarketCap": stock.ocfToMarketCap,
        "ocfPerShare": stock.ocfPerShare,
        "ocfToEV": stock.ocfToEV
    } for stock in stocks])


@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    try:
        stock = StockModel.query.get(stock_id)
        if not stock:
            return jsonify({"error": "Stock not found"}), 404

        db.session.delete(stock)
        db.session.commit()

        return jsonify({"message": "Stock deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting stock: {e}")
        return jsonify({"error": "Error deleting stock"}), 500


if __name__ == "__main__":
    app.run(debug=True)