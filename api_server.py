from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/api/top10/<year>')
def top10(year):
    with sqlite3.connect('FORTUNE500.db') as con:
        cur = con.cursor()

        query = ""
        if year == 'all-time':
            query = """
                select c.company_id, company_name, sum(revenue_mil) revenue
                from yearly_data yd
                join companies c on c.company_id = yd.company_id
                group by company_name
                order by sum(revenue_mil) desc
                limit 10
            """
        else:
            query = f"""
                select c.company_id, company_name, revenue_mil revenue
                from yearly_data yd
                join companies c on c.company_id = yd.company_id
                where year = {year}
                order by revenue_mil desc
                limit 10
            """
        
        cur.execute(query)
        json_data = []
        for row in cur:
            company_id, company, revenue = row
            json_data.append({ 'company_id': company_id,
                                'company': company,
                                 'revenue': revenue })

        return jsonify(json_data)
    
@app.route('/api/company/<company_id>')
def company(company_id):
    with sqlite3.connect('FORTUNE500.db') as con:
        cur = con.cursor()

        query = f"""
            select company_name, year, revenue_mil
            from yearly_data yd
            join companies c on c.company_id = yd.company_id
            where c.company_id = '{company_id}'
            order by year
        """

        cur.execute(query)
        company_name = ""
        x = []
        y = []
        for row in cur:
            company_name = row[0]
            x.append(row[1])
            y.append(row[2])

        return jsonify({ 'company_name': company_name, 'x': x, 'y': y })

if __name__ == '__main__':
    app.run(debug=True)