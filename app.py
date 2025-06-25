from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random
import json

app = Flask(__name__)
CORS(app)


class BankingAssistant:
    def __init__(self):
        self.banking_keywords = [
            'cont', 'sold', 'tranzactie', 'transfer', 'credit', 'debit', 'card',
            'factura', 'plata', 'salariu', 'rata', 'dobanda', 'investitie', 'investit',
            'ebitda', 'profit', 'cash', 'numerar', 'flux', 'rating', 'risc',
            'buget', 'cheltuieli', 'venituri', 'bilant', 'raport', 'financiar',
            'banca', 'bancar', 'economii', 'depozit', 'imprumut', 'comision',
            'curs', 'valuta', 'euro', 'dolar', 'ron', 'leu', 'moneda',
            'trezorerie', 'lichiditate', 'capital', 'activ', 'pasiv',
            'dividend', 'actionar', 'garantie', 'aval', 'scadenta', 'calcul',
            'calculate', 'calculeaza', 'formula', 'metrici', 'kpi', 'roi',
            'strategi', 'strategii', 'portofoliu', 'companie', 'companii', 'firma',
            'afacere', 'afaceri', 'business', 'bani', 'financiare', 'economic',
            'castig', 'pierdere', 'optimizare', 'recomandari', 'analiza'
        ]

        self.non_banking_responses = [
            "Îmi pare rău, sunt un asistent financiar specializat și pot răspunde doar la întrebări legate de servicii bancare și financiare.",
            "Nu pot să te ajut cu această întrebare. Sunt programat să asist doar cu informații bancare și financiare.",
            "Această întrebare nu este în domeniul meu de expertiză. Te pot ajuta cu aspecte legate de banking, finanțe și managementul banilor.",
            "Din păcate, pot oferi suport doar pentru întrebări bancare și financiare. Reformulează întrebarea dacă este legată de aceste domenii."
        ]

        # Date simulate pentru calculele demo
        self.company_data = {
            'revenue': 2500000,  # Venituri
            'operating_costs': 1800000,  # Costuri operaționale
            'depreciation': 150000,  # Amortizare
            'interest': 45000,  # Dobânzi
            'taxes': 85000,  # Taxe
            'total_assets': 3200000,  # Active totale
            'current_assets': 1200000,  # Active circulante
            'current_liabilities': 800000,  # Datorii pe termen scurt
            'total_debt': 1400000,  # Datorii totale
            'equity': 1800000,  # Capitaluri proprii
            'cash': 320000,  # Numerar disponibil
            'employees': 24,  # Numărul de angajați
            'market_sector': 'tehnologie'  # Sectorul de activitate
        }

        self.investment_strategies = {
            'conservativ': {
                'profile': 'Risc scăzut, rentabilitate moderată',
                'options': [
                    {'name': 'Depozite bancare', 'roi': '2-4%', 'risk': 'Foarte scăzut'},
                    {'name': 'Obligațiuni corporative', 'roi': '4-6%', 'risk': 'Scăzut'},
                    {'name': 'Fonduri monetare', 'roi': '3-5%', 'risk': 'Scăzut'}
                ]
            },
            'moderat': {
                'profile': 'Echilibru între risc și rentabilitate',
                'options': [
                    {'name': 'Fonduri mixte', 'roi': '6-10%', 'risk': 'Mediu'},
                    {'name': 'ETF-uri diversificate', 'roi': '8-12%', 'risk': 'Mediu'},
                    {'name': 'Investiții imobiliare', 'roi': '7-15%', 'risk': 'Mediu'}
                ]
            },
            'agresiv': {
                'profile': 'Risc ridicat, potențial de rentabilitate mare',
                'options': [
                    {'name': 'Acțiuni tehnologie', 'roi': '12-25%', 'risk': 'Ridicat'},
                    {'name': 'Start-up investments', 'roi': '15-40%', 'risk': 'Foarte ridicat'},
                    {'name': 'Crypto assets', 'roi': '10-50%', 'risk': 'Extrem de ridicat'}
                ]
            }
        }

        self.responses = {
            'ebitda_calc': {
                'response': self.calculate_ebitda,
                'tips': [
                    "EBITDA oferă o imagine clară a performanței operaționale",
                    "O marjă EBITDA >15% este considerată bună pentru majoritatea industriilor",
                    "Compară EBITDA-ul cu companiile din același sector",
                    "Monitorizează tendința EBITDA pe mai multe trimestre"
                ]
            },

            'rating_calc': {
                'response': self.calculate_credit_rating,
                'tips': [
                    "Rating-ul se bazează pe mai mulți factori financiari",
                    "Un rating A sau superior oferă acces la credite preferențiale",
                    "Îmbunătățește rating-ul prin reducerea datoriilor",
                    "Menține un istoric de plăți impecabil"
                ]
            },

            'ratii_financiare': {
                'response': self.calculate_financial_ratios,
                'tips': [
                    "Ratiile financiare oferă o perspectivă completă asupra sănătății financiare",
                    "Compară ratiile cu media industriei pentru context",
                    "Monitorizează evoluția ratiilor în timp",
                    "Folosește ratiile pentru planificarea strategică"
                ]
            },

            'strategii_investitii': {
                'response': self.get_investment_strategies,
                'tips': [
                    "Diversifică portofoliul pentru reducerea riscului",
                    "Aliniază strategia cu obiectivele pe termen lung",
                    "Rebalanseaza portofoliul trimestrial",
                    "Consideră impactul fiscal al investițiilor"
                ]
            },

            'analiza_risc': {
                'response': self.analyze_risk_profile,
                'tips': [
                    "Identifică și monitorizează riscurile principale",
                    "Creează planuri de contingență pentru scenarii negative",
                    "Diversifică pentru reducerea concentrării riscului",
                    "Revizuiește profilul de risc lunar"
                ]
            },

            'recomandari_optimizare': {
                'response': self.get_optimization_recommendations,
                'tips': [
                    "Implementează recomandările pas cu pas",
                    "Măsoară impactul fiecărei optimizări",
                    "Prioritizează acțiunile cu ROI ridicat",
                    "Monitorizează progresul lunar"
                ]
            }
        }

    def calculate_ebitda(self):
        data = self.company_data

        # EBITDA = Venituri - Costuri operaționale + Depreciere + Amortizare + Dobânzi + Taxe
        ebitda = data['revenue'] - data['operating_costs']
        net_profit = ebitda - data['depreciation'] - data['interest'] - data['taxes']
        ebitda_margin = (ebitda / data['revenue']) * 100

        # Evaluare performanță
        if ebitda_margin >= 20:
            performance = "Excelentă"
        elif ebitda_margin >= 15:
            performance = "Bună"
        elif ebitda_margin >= 10:
            performance = "Acceptabilă"
        else:
            performance = "Sub media industriei"

        return [
            f"📊 ANALIZA EBITDA PENTRU COMPANIA TA",
            f"",
            f"💰 Venituri totale: {data['revenue']:,} RON",
            f"💸 Costuri operaționale: {data['operating_costs']:,} RON",
            f"",
            f"🔹 EBITDA calculat: {ebitda:,} RON",
            f"🔹 Marja EBITDA: {ebitda_margin:.1f}%",
            f"🔹 Profit net: {net_profit:,} RON",
            f"",
            f"📈 Evaluare performanță: {performance}",
            f"🎯 Pentru sectorul {data['market_sector']}, ținta recomandată este 15-25%"
        ]

    def calculate_credit_rating(self):
        data = self.company_data

        # Calculăm ratiile cheie pentru rating
        debt_to_equity = data['total_debt'] / data['equity']
        current_ratio = data['current_assets'] / data['current_liabilities']
        debt_service_coverage = (data['revenue'] - data['operating_costs']) / (
                data['interest'] + (data['total_debt'] * 0.1))  # Estimare plăți principale

        # Calculăm scorul (simplificat)
        score = 0

        # Debt-to-Equity (30% din scor)
        if debt_to_equity < 0.3:
            score += 30
        elif debt_to_equity < 0.5:
            score += 25
        elif debt_to_equity < 0.8:
            score += 20
        else:
            score += 10

        # Current Ratio (25% din scor)
        if current_ratio > 2.0:
            score += 25
        elif current_ratio > 1.5:
            score += 20
        elif current_ratio > 1.2:
            score += 15
        else:
            score += 5

        # Debt Service Coverage (25% din scor)
        if debt_service_coverage > 3.0:
            score += 25
        elif debt_service_coverage > 2.0:
            score += 20
        elif debt_service_coverage > 1.5:
            score += 15
        else:
            score += 5

        # Profitabilitate (20% din scor)
        profit_margin = ((data['revenue'] - data['operating_costs'] - data['depreciation']) / data['revenue']) * 100
        if profit_margin > 15:
            score += 20
        elif profit_margin > 10:
            score += 15
        elif profit_margin > 5:
            score += 10
        else:
            score += 5

        # Determinăm rating-ul
        if score >= 90:
            rating = "AAA (Excelent)"
        elif score >= 80:
            rating = "AA (Foarte bun)"
        elif score >= 70:
            rating = "A (Bun)"
        elif score >= 60:
            rating = "BBB (Acceptabil)"
        elif score >= 50:
            rating = "BB (Sub medie)"
        else:
            rating = "B (Risc ridicat)"

        return [
            f"🏆 EVALUARE RATING DE CREDIT",
            f"",
            f"📊 Ratii financiare cheie:",
            f"• Debt-to-Equity: {debt_to_equity:.2f}",
            f"• Current Ratio: {current_ratio:.2f}",
            f"• Debt Service Coverage: {debt_service_coverage:.2f}",
            f"• Marja de profit: {profit_margin:.1f}%",
            f"",

            f"",
            f"💡 Pentru îmbunătățire, focusează-te pe reducerea datoriilor și creșterea profitabilității"
        ]

    def calculate_financial_ratios(self):
        data = self.company_data

        # Calculăm ratiile importante
        ratios = {
            'lichiditate_curenta': data['current_assets'] / data['current_liabilities'],
            'lichiditate_rapida': (data['current_assets'] - 200000) / data['current_liabilities'],  # Estimare stocuri
            'debt_to_assets': data['total_debt'] / data['total_assets'],
            'debt_to_equity': data['total_debt'] / data['equity'],
            'asset_turnover': data['revenue'] / data['total_assets'],
            'roi': ((data['revenue'] - data['operating_costs'] - data['depreciation']) / data['total_assets']) * 100,
            'roe': ((data['revenue'] - data['operating_costs'] - data['depreciation']) / data['equity']) * 100
        }

        return [
            f"📈 ANALIZA RATIILOR FINANCIARE",
            f"",
            f"💧 RATII DE LICHIDITATE:",
            f"• Lichiditate curentă: {ratios['lichiditate_curenta']:.2f} (optim: >1.5)",
            f"• Lichiditate rapidă: {ratios['lichiditate_rapida']:.2f} (optim: >1.0)",
            f"",
            f"💳 RATII DE ÎNDATORARE:",
            f"• Debt-to-Assets: {ratios['debt_to_assets']:.2f} (optim: <0.4)",
            f"• Debt-to-Equity: {ratios['debt_to_equity']:.2f} (optim: <0.5)",
            f"",
            f"⚡ RATII DE EFICIENȚĂ:",
            f"• Asset Turnover: {ratios['asset_turnover']:.2f}x",
            f"• ROI: {ratios['roi']:.1f}% (optim: >10%)",
            f"• ROE: {ratios['roe']:.1f}% (optim: >15%)",
            f"",
            f"🎯 Ratiile tale sunt în parametri {'normali' if ratios['debt_to_equity'] < 0.6 else 'atenție la îndatorare'}"
        ]

    def get_investment_strategies(self):
        data = self.company_data

        # Determinăm profilul bazat pe situația financiară
        debt_ratio = data['total_debt'] / data['total_assets']
        cash_ratio = data['cash'] / data['current_liabilities']

        if debt_ratio < 0.3 and cash_ratio > 0.5:
            profile_type = 'agresiv'
            risk_capacity = "Ridicată"
        elif debt_ratio < 0.5 and cash_ratio > 0.3:
            profile_type = 'moderat'
            risk_capacity = "Medie"
        else:
            profile_type = 'conservativ'
            risk_capacity = "Scăzută"

        strategy = self.investment_strategies[profile_type]

        response = [
            f"🎯 STRATEGII DE INVESTIȚII PERSONALIZATE",
            f"",
            f"📊 Analiza profilului financiar:",
            f"• Capacitate de risc: {risk_capacity}",
            f"• Profil recomandat: {profile_type.upper()}",
            f"• Disponibil pentru investiții: {data['cash']:,} RON",
            f"",
            f"💼 {strategy['profile']}",
            f""
        ]

        for i, option in enumerate(strategy['options'], 1):
            response.append(f"{i}. {option['name']}")
            response.append(f"   • ROI estimat: {option['roi']}")
            response.append(f"   • Nivel risc: {option['risk']}")
            response.append("")

        # Recomandări personalizate bazate pe sectorul de activitate
        if data['market_sector'] == 'tehnologie':
            response.extend([
                "🚀 RECOMANDĂRI SECTORIALE:",
                "• Investiții în R&D: 15-20% din profit",
                "• Tehnologii emergente (AI, blockchain)",
                "• Expansiune digitală și automatizare"
            ])

        return response

    def analyze_risk_profile(self):
        data = self.company_data

        risks = []
        risk_score = 0

        # Analizăm diverse tipuri de risc
        debt_ratio = data['total_debt'] / data['total_assets']
        if debt_ratio > 0.6:
            risks.append("🔴 Risc de îndatorare ridicat")
            risk_score += 3
        elif debt_ratio > 0.4:
            risks.append("🟡 Risc de îndatorare moderat")
            risk_score += 2
        else:
            risks.append("🟢 Risc de îndatorare scăzut")
            risk_score += 1

        current_ratio = data['current_assets'] / data['current_liabilities']
        if current_ratio < 1.2:
            risks.append("🔴 Risc de lichiditate ridicat")
            risk_score += 3
        elif current_ratio < 1.5:
            risks.append("🟡 Risc de lichiditate moderat")
            risk_score += 2
        else:
            risks.append("🟢 Lichiditate bună")
            risk_score += 1

        # Risc de concentrare (simulat)
        risks.append("🟡 Risc de concentrare - diversifică clienții")
        risk_score += 2

        if risk_score <= 4:
            overall_risk = "SCĂZUT"
        elif risk_score <= 7:
            overall_risk = "MODERAT"
        else:
            overall_risk = "RIDICAT"

        return [
            f"⚠️ PROFIL DE RISC FINANCIAR",
            f"",
            f"📊 Scor total risc: {risk_score}/9",
            f"🎯 Nivel general: {overall_risk}",
            f"",
            f"📋 Analiza detaliată:"
        ] + risks + [
            f"",
            f"🛡️ Măsuri de protecție recomandate:",
            f"• Asigurare corporativă completă",
            f"• Fond de rezervă 6 luni cheltuieli",
            f"• Diversificare portofoliu clienți",
            f"• Contracte cu clauze de protecție"
        ]

    def get_optimization_recommendations(self):
        data = self.company_data

        recommendations = [
            f"🎯 RECOMANDĂRI DE OPTIMIZARE FINANCIARĂ",
            f"",
            f"💡 TOP PRIORITĂȚI PENTRU COMPANIA TA:"
        ]

        # Recomandări bazate pe analiza datelor
        debt_ratio = data['total_debt'] / data['equity']
        if debt_ratio > 0.8:
            recommendations.extend([
                "",
                "🔥 PRIORITATE MAXIMĂ - Reducerea datoriilor:",
                f"• Datorii actuale: {data['total_debt']:,} RON",
                f"• Țintă recomandată: {int(data['equity'] * 0.5):,} RON",
                f"• Economie anuală dobânzi: ~{int(data['total_debt'] * 0.05):,} RON"
            ])

        ebitda = data['revenue'] - data['operating_costs']
        ebitda_margin = (ebitda / data['revenue']) * 100
        if ebitda_margin < 15:
            recommendations.extend([
                "",
                "📈 Îmbunătățirea profitabilității:",
                f"• Marja actuală EBITDA: {ebitda_margin:.1f}%",
                f"• Țintă industrială: 15-20%",
                f"• Potențial creștere profit: {int((data['revenue'] * 0.18) - ebitda):,} RON"
            ])

        recommendations.extend([
            "",
            "🚀 PLANUL DE ACȚIUNE (6 LUNI):",
            "",
            "LUNA 1-2: Optimizare costuri",
            "• Audit furnizori și renegociere contracte",
            "• Automatizare procese repetitive",
            "• Eficientizare echipă (training, tools)",
            "",
            "LUNA 3-4: Îmbunătățire venituri",
            "• Diversificare produse/servicii",
            "• Optimizare prețuri și pachete",
            "• Strategie marketing digitală",
            "",
            "LUNA 5-6: Consolidare financiară",
            "• Restructurare datorii (dacă necesară)",
            "• Implementare sistem de monitoring",
            "• Planificare investiții strategice"
        ])

        return recommendations

    def is_banking_related(self, message):
        message_lower = message.lower()

        # Verificăm dacă mesajul conține cuvinte cheie bancare
        banking_score = sum(1 for keyword in self.banking_keywords if keyword in message_lower)

        # Adăugăm verificări suplimentare pentru expresii comune
        banking_phrases = [
            'strategi', 'investit', 'portofoliu', 'profit', 'castig',
            'bani', 'financiar', 'economic', 'afacer', 'compani',
            'firma', 'business', 'venit', 'cheltuiel', 'sold',
            'calcul', 'ebitda', 'rating', 'risc', 'ratii'
        ]

        phrase_score = sum(1 for phrase in banking_phrases if phrase in message_lower)

        # Debug info
        print(f"Message: {message_lower}")
        print(f"Banking score: {banking_score}")
        print(f"Phrase score: {phrase_score}")
        print(f"Total relevant: {banking_score + phrase_score > 0}")

        return (banking_score + phrase_score) > 0

    def get_response_category(self, message):
        message_lower = message.lower()

        # Categorii cu calcule
        if any(word in message_lower for word in ['calcul', 'calculate', 'calculeaza']) and 'ebitda' in message_lower:
            return 'ebitda_calc'
        elif any(word in message_lower for word in ['calcul', 'calculate', 'calculeaza']) and any(
                word in message_lower for word in ['rating', 'scor', 'credit']):
            return 'rating_calc'
        elif any(word in message_lower for word in ['ratii', 'ratio', 'metrici', 'kpi']):
            return 'ratii_financiare'
        elif any(word in message_lower for word in ['strategi', 'investit', 'portofoliu']):
            return 'strategii_investitii'
        elif any(word in message_lower for word in ['risc', 'riscuri', 'sigur']):
            return 'analiza_risc'
        elif any(word in message_lower for word in ['optimiz', 'imbunatatir', 'recomand']):
            return 'recomandari_optimizare'

        # Categorii clasice
        categories = {
            'ebitda': ['ebitda', 'profit', 'castig', 'rentabilitate', 'marja'],
            'rating': ['rating', 'credit', 'scor', 'evaluare', 'punctaj'],
            'cash_flow': ['flux', 'numerar', 'cash', 'lichiditate', 'circulant'],
            'investitii': ['investit', 'dezvoltare', 'crestere', 'expansiune'],
            'credit': ['credit', 'imprumut', 'finantare', 'fonduri'],
            'buget': ['buget', 'planificare', 'alocare', 'cheltuieli'],
            'risc': ['risc', 'siguranta', 'protectie', 'asigurare'],
            'rapoarte': ['raport', 'analize', 'statistic', 'performant'],
            'dobanda': ['dobanda', 'rata', 'procent', 'cost'],
            'valuta': ['valuta', 'curs', 'schimb', 'euro', 'dolar']
        }

        for category, keywords in categories.items():
            if any(keyword in message_lower for keyword in keywords):
                return category

        return 'general'

    def generate_response(self, message):
        if not self.is_banking_related(message):
            return {
                'response': random.choice(self.non_banking_responses),
                'tips': [
                    "Întreabă: 'Calculează EBITDA-ul companiei'",
                    "Solicită: 'Care este rating-ul meu de credit?'",
                    "Cere: 'Analizează ratiile financiare'",
                    "Discută: 'Strategii de investiții pentru compania mea'",
                    "Află: 'Recomandări de optimizare financiară'"
                ]
            }

        category = self.get_response_category(message)

        if category in self.responses:
            response_data = self.responses[category]
            if callable(response_data['response']):
                # Pentru funcțiile de calcul
                calculated_response = response_data['response']()
                return {
                    'response': calculated_response,
                    'tips': response_data['tips']
                }
            else:
                return response_data
        else:
            return {
                'response': [
                    "Înțeleg că întrebarea ta este legată de aspecte financiare.",
                    "Iată câteva sfaturi generale pentru o gestionare financiară eficientă:"
                ],
                'tips': [
                    "Monitorizează constant fluxul de numerar",
                    "Menține un raport sănătos între datorii și capitaluri proprii",
                    "Investește în tehnologii care reduc costurile",
                    "Diversifică sursele de venit pentru stabilitate",
                    "Planifică bugetul pe baza datelor istorice și prognoze realiste"
                ]
            }


assistant = BankingAssistant()


@app.route('/api/analysis', methods=['GET'])
def health_check():
    return jsonify({'status': 'online', 'service': 'BT-GO Banking Assistant with Calculations'})


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        response = assistant.generate_response(message)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🏦 BT-GO Banking Assistant Server Starting...")
    print("🧮 Cu funcționalități avansate de calcule financiare")
    print("📊 EBITDA | 🏅 Rating Credit | 📈 Ratii | 💼 Investiții")
    print("🚀 Server disponibil pe http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)