from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BT-GO - Banking Corporativ Digital</title>
    <style>
        :root {
            --bt-blue: #003366;
            --bt-light-blue: #4A90C2;
            --bt-beige: #F5F1E8;
            --bt-yellow: #FFD700;
            --bt-red: #DC143C;
            --bt-dark-blue: #002244;
            --bt-gray: #6B7280;
            --bt-light-gray: #F8F9FA;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bt-blue) 0%, var(--bt-light-blue) 50%, var(--bt-dark-blue) 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .header {
            background: rgba(245, 241, 232, 0.95);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            padding: 15px 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            animation: slideDown 0.8s ease-out;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--bt-blue);
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            margin-right: 10px;
            font-size: 1.2rem;
        }

        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        .nav-links a {
            color: #374151;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            padding: 8px 16px;
            border-radius: 8px;
        }

        .nav-links a:hover {
            background: var(--bt-beige);
            color: var(--bt-blue);
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--bt-light-gray);
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
        }

        .main-content {
            margin-top: 80px;
            padding: 40px 0;
        }

        .hero {
            text-align: center;
            color: white;
            margin-bottom: 50px;
            animation: fadeInUp 1s ease-out;
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .hero p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }

        .account-overview {
            background: rgba(245, 241, 232, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            animation: slideInLeft 0.8s ease-out;
        }

        .balance-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .balance-card {
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            color: white;
            padding: 25px;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease;
        }

        .balance-card:hover {
            transform: translateY(-5px);
        }

        .balance-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            transition: all 0.5s ease;
        }

        .balance-card:hover::before {
            transform: scale(1.5);
        }

        .balance-label {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 8px;
        }

        .balance-amount {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .balance-change {
            font-size: 0.85rem;
            opacity: 0.9;
        }

        .positive { color: var(--bt-yellow); }
        .negative { color: var(--bt-red); }

        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .action-btn {
            background: white;
            border: 2px solid #e2e8f0;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: #374151;
        }

        .action-btn:hover {
            border-color: var(--bt-blue);
            background: var(--bt-beige);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 51, 102, 0.15);
        }

        .action-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
            display: block;
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }

        .dashboard-card {
            background: rgba(245, 241, 232, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            animation: slideInUp 0.8s ease-out;
        }

        .dashboard-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px rgba(0,0,0,0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
        }

        .transactions-icon { background: linear-gradient(135deg, var(--bt-light-blue), var(--bt-blue)); }
        .reports-icon { background: linear-gradient(135deg, var(--bt-yellow), #DAA520); }
        .invoices-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .payroll-icon { background: linear-gradient(135deg, var(--bt-red), #B22222); }
        .treasury-icon { background: linear-gradient(135deg, var(--bt-blue), var(--bt-dark-blue)); }
        .cards-icon { background: linear-gradient(135deg, var(--bt-light-blue), var(--bt-blue)); }

        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--bt-dark-blue);
            margin: 0;
        }

        .card-subtitle {
            color: var(--bt-gray);
            font-size: 0.9rem;
        }

        .card-content {
            color: #4b5563;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .card-stats {
            display: flex;
            justify-content: space-between;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--bt-blue);
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--bt-gray);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 51, 102, 0.3);
        }

        .recent-activity {
            background: rgba(245, 241, 232, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        .activity-item {
            display: flex;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #f3f4f6;
        }

        .activity-item:last-child {
            border-bottom: none;
        }

        .activity-icon {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.1rem;
        }

        .activity-details {
            flex: 1;
        }

        .activity-title {
            font-weight: 500;
            color: var(--bt-dark-blue);
        }

        .activity-time {
            font-size: 0.85rem;
            color: var(--bt-gray);
        }

        .activity-amount {
            font-weight: 600;
            color: var(--bt-blue);
        }

        .assistant-fab {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            box-shadow: 0 15px 35px rgba(0, 51, 102, 0.4);
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
            animation: pulse 2s infinite;
            border: none;
        }

        .assistant-fab:hover {
            transform: scale(1.1);
            box-shadow: 0 20px 45px rgba(0, 51, 102, 0.5);
        }

        .chat-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            z-index: 2000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .chat-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .chat-container {
            position: fixed;
            bottom: 120px;
            right: 30px;
            width: 400px;
            height: 600px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            transform: translateY(100px) scale(0.8);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 2001;
            display: flex;
            flex-direction: column;
        }

        .chat-container.active {
            transform: translateY(0) scale(1);
            opacity: 1;
        }

        .chat-header {
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .chat-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }

        .chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }

        .chat-close:hover {
            opacity: 1;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .message.user {
            align-self: flex-end;
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            color: white;
        }

        .message.assistant {
            align-self: flex-start;
            background: var(--bt-beige);
            color: #374151;
            border: 1px solid #e2e8f0;
        }

        .message.assistant .tips {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
            font-size: 0.85rem;
            color: var(--bt-gray);
        }

        .message.assistant .tips ul {
            margin: 5px 0;
            padding-left: 15px;
        }

        .typing-indicator {
            align-self: flex-start;
            padding: 12px 16px;
            background: var(--bt-beige);
            border-radius: 18px;
            border: 1px solid #e2e8f0;
            display: none;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--bt-gray);
            animation: typing 1.4s infinite;
        }

        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }

        .chat-input-container {
            padding: 20px;
            border-top: 1px solid #e2e8f0;
            border-radius: 0 0 20px 20px;
        }

        .chat-input-wrapper {
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }

        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 0.9rem;
            resize: none;
            outline: none;
            transition: border-color 0.3s ease;
            min-height: 20px;
            max-height: 100px;
        }

        .chat-input:focus {
            border-color: var(--bt-blue);
        }

        .chat-send {
            background: linear-gradient(135deg, var(--bt-blue), var(--bt-light-blue));
            color: white;
            border: none;
            padding: 12px 16px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-send:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 51, 102, 0.3);
        }

        .chat-send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .quick-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }

        .suggestion-btn {
            background: var(--bt-beige);
            border: 1px solid #e2e8f0;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #374151;
        }

        .suggestion-btn:hover {
            background: #e2e8f0;
            border-color: var(--bt-blue);
            color: var(--bt-blue);
        }

        .assistant-status {
            position: absolute;
            top: -8px;
            right: -8px;
            width: 20px;
            height: 20px;
            background: var(--bt-yellow);
            border: 3px solid white;
            border-radius: 50%;
            animation: pulse-status 2s infinite;
        }

        .api-config-panel {
            position: fixed;
            top: 90px;
            right: 20px;
            background: rgba(245, 241, 232, 0.98);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            width: 350px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            z-index: 1001;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        }

        .api-config-panel.active {
            transform: translateX(0);
        }

        .config-toggle {
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--bt-blue);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            z-index: 1002;
            transition: all 0.3s ease;
        }

        .config-toggle:hover {
            background: var(--bt-dark-blue);
            transform: scale(1.05);
        }

        .config-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--bt-dark-blue);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .config-group {
            margin-bottom: 15px;
        }

        .config-label {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--bt-gray);
            margin-bottom: 5px;
        }

        .config-input {
            width: 100%;
            padding: 10px 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: border-color 0.3s ease;
        }

        .config-input:focus {
            border-color: var(--bt-blue);
            outline: none;
        }

        .config-status {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            margin-top: 5px;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #ef4444;
        }

        .status-indicator.online {
            background: #10b981;
        }

        .env-badge {
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--bt-blue);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            z-index: 1001;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        @keyframes slideDown {
            from { transform: translateY(-100%); }
            to { transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes pulse-status {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }

        .bg-shapes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }

        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 215, 0, 0.1);
            animation: float 8s infinite ease-in-out;
        }

        .shape:nth-child(1) {
            width: 200px;
            height: 200px;
            top: 10%;
            left: 80%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            width: 150px;
            height: 150px;
            top: 70%;
            left: 10%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            width: 100px;
            height: 100px;
            top: 30%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }

            .hero h1 {
                font-size: 2.2rem;
            }

            .balance-cards {
                grid-template-columns: 1fr;
            }

            .dashboard {
                grid-template-columns: 1fr;
            }

            .quick-actions {
                grid-template-columns: repeat(2, 1fr);
            }

            .chat-container {
                width: 90%;
                right: 5%;
                left: 5%;
                bottom: 100px;
                height: 70vh;
            }

            .api-config-panel {
                width: 90%;
                right: 5%;
                left: 5%;
            }

            .config-toggle {
                right: 5%;
            }
        }

        @media (max-width: 480px) {
            .quick-actions {
                grid-template-columns: 1fr;
            }

            .chat-container {
                height: 80vh;
                bottom: 80px;
            }
        }
    </style>
</head>
<body>
    <div class="env-badge">
        <span>🌐</span>
        <span>BT-GO Production</span>
    </div>

    <button class="config-toggle" id="configToggle">⚙️ API Config</button>

    <div class="api-config-panel" id="configPanel">
        <div class="config-title">
            <span>🔧</span>
            <span>Configurare API Endpoints</span>
        </div>
        
        <div class="config-group">
            <label class="config-label" for="assistantUrl">Assistant API URL:</label>
            <input type="url" class="config-input" id="assistantUrl" placeholder="https://your-assistant-api.com">
            <div class="config-status">
                <div class="status-indicator" id="assistantStatus"></div>
                <span id="assistantStatusText">Offline</span>
            </div>
        </div>

        <div class="config-group">
            <label class="config-label" for="reportsUrl">Reports API URL:</label>
            <input type="url" class="config-input" id="reportsUrl" placeholder="https://your-reports-api.com">
            <div class="config-status">
                <div class="status-indicator" id="reportsStatus"></div>
                <span id="reportsStatusText">Offline</span>
            </div>
        </div>
    </div>

    <div class="bg-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>

    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">
                    <div class="logo-icon">🏦</div>
                    BT-GO Business
                </div>
                <ul class="nav-links">
                    <li><a href="#dashboard">Dashboard</a></li>
                    <li><a href="#tranzactii">Tranzacții</a></li>
                    <li><a href="#rapoarte">Rapoarte</a></li>
                    <li><a href="#servicii">Servicii</a></li>
                    <li><a href="#ajutor">Ajutor</a></li>
                </ul>
                <div class="user-profile">
                    <span>👤</span>
                    <span>SC DEMO SRL</span>
                </div>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <section class="hero">
                <h1>Banca Digitală pentru Afacerea Ta</h1>
                <p>Gestionează toate operațiunile financiare ale companiei într-un singur loc</p>
            </section>

            <section class="account-overview">
                <h2 style="margin-bottom: 25px; color: #1f2937;">Prezentare Conturi</h2>
                
                <div class="balance-cards">
                    <div class="balance-card">
                        <div class="balance-label">Cont de Economii</div>
                        <div class="balance-amount">89,234.67 RON</div>
                        <div class="balance-change positive">+2,456 RON (2.8%)</div>
                    </div>
                    <div class="balance-card">
                        <div class="balance-label">Cont în EUR</div>
                        <div class="balance-amount">15,678.90 EUR</div>
                        <div class="balance-change negative">-234 EUR (-1.5%)</div>
                    </div>
                </div>

                <div class="quick-actions">
                    <a href="#" class="action-btn">
                        <span class="action-icon">💸</span>
                        Transfer Rapid
                    </a>
                    <a href="#" class="action-btn">
                        <span class="action-icon">📄</span>
                        Plată Factură
                    </a>
                    <a href="#" class="action-btn">
                        <span class="action-icon">👥</span>
                        Plată Salarii
                    </a>
                    <a href="#" class="action-btn">
                        <span class="action-icon">📊</span>
                        Export Extras
                    </a>
                    <a href="#" class="action-btn">
                        <span class="action-icon">🔄</span>
                        Conversie Valută
                    </a>
                </div>
            </section>

            <section class="dashboard">
                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon transactions-icon">💳</div>
                        <div>
                            <h3 class="card-title">Tranzacții</h3>
                            <p class="card-subtitle">Istoric și management</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Vizualizează toate tranzacțiile, filtrează după criterii și exportă datele pentru contabilitate.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">149</div>
                            <div class="stat-label">Efectuate</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Respinse</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">14</div>
                            <div class="stat-label">În așteptare</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary">Configurează</a>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon reports-icon">📈</div>
                        <div>
                            <h3 class="card-title">Rapoarte Financiare</h3>
                            <p class="card-subtitle">Analiză și statistici</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Generează rapoarte detaliate pentru analiza fluxului de numerar și performanța financiară.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">23</div>
                            <div class="stat-label">Rapoarte</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">8</div>
                            <div class="stat-label">Programate</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">156</div>
                            <div class="stat-label">Exporturi</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary" id="reportsBtn">Generează</a>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon treasury-icon">🏛️</div>
                        <div>
                            <h3 class="card-title">Trezorerie</h3>
                            <p class="card-subtitle">Cash management</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Optimizează fluxul de numerar, gestionează depozitele și investițiile pe termen scurt.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">3</div>
                            <div class="stat-label">Depozite</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">2.1%</div>
                            <div class="stat-label">Rata anuală</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">45k</div>
                            <div class="stat-label">Disponibil</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary">Investește</a>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon cards-icon">💳</div>
                        <div>
                            <h3 class="card-title">Carduri Corporative</h3>
                            <p class="card-subtitle">Management și control</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Gestionează cardurile de debit și credit ale companiei. Setează limite și monitorizează cheltuielile.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">8</div>
                            <div class="stat-label">Active</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">12.3k</div>
                            <div class="stat-label">Cheltuit</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">87.7k</div>
                            <div class="stat-label">Disponibil</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary">Administrează</a>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon invoices-icon">🧾</div>
                        <div>
                            <h3 class="card-title">Facturare</h3>
                            <p class="card-subtitle">Emitere și tracking</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Creează, trimite și urmărește facturile. Automatizează procesul de facturare recurentă.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">67</div>
                            <div class="stat-label">Emise</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">12</div>
                            <div class="stat-label">Neplatite</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">3</div>
                            <div class="stat-label">Restante</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary">Administrează</a>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-icon payroll-icon">💰</div>
                        <div>
                            <h3 class="card-title">Gestiune Salarii</h3>
                            <p class="card-subtitle">Plăți automate</p>
                        </div>
                    </div>
                    <div class="card-content">
                        Automatizează plata salariilor și contribuțiilor. Gestionează toate aspectele HR financiare.
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-number">24</div>
                            <div class="stat-label">Angajați</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">89.5k</div>
                            <div class="stat-label">Total RON</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">15</div>
                            <div class="stat-label">Zile până</div>
                        </div>
                    </div>
                    <br>
                    <a href="#" class="btn-primary">Configurează</a>
                </div>
            </section>

            <section class="recent-activity">
                <h2 style="margin-bottom: 25px; color: #1f2937;">Activitate Recentă</h2>
                
                <div class="activity-item">
                    <div class="activity-icon" style="background: #10b981; color: white;">↓</div>
                    <div class="activity-details">
                        <div class="activity-title">Transfer primit - CLIENTE ABC SRL</div>
                        <div class="activity-time">Astăzi, 14:32</div>
                    </div>
                    <div class="activity-amount">+15,420.00 RON</div>
                </div>

                <div class="activity-item">
                    <div class="activity-icon" style="background: #ef4444; color: white;">↑</div>
                    <div class="activity-details">
                        <div class="activity-title">Plată factură - FURNIZOR XYZ</div>
                        <div class="activity-time">Astăzi, 11:45</div>
                    </div>
                    <div class="activity-amount">-8,750.50 RON</div>
                </div>

                <div class="activity-item">
                    <div class="activity-icon" style="background: #f59e0b; color: white;">💳</div>
                    <div class="activity-details">
                        <div class="activity-title">Plată cu cardul corporativ - Combustibil</div>
                        <div class="activity-time">Ieri, 16:20</div>
                    </div>
                    <div class="activity-amount">-245.60 RON</div>
                </div>

                <div class="activity-item">
                    <div class="activity-icon" style="background: #8b5cf6; color: white;">👥</div>
                    <div class="activity-details">
                        <div class="activity-title">Plată salarii - Noiembrie 2024</div>
                        <div class="activity-time">25 Nov, 10:00</div>
                    </div>
                    <div class="activity-amount">-89,420.00 RON</div>
                </div>
            </section>
        </div>
    </main>

    <button class="assistant-fab" id="assistantBtn" title="Asistent Virtual Bancar">
        🤖
        <div class="assistant-status"></div>
    </button>

    <div class="chat-overlay" id="chatOverlay">
        <div class="chat-container" id="chatContainer">
            <div class="chat-header">
                <div class="chat-title">
                    <span>🤖</span>
                    <span>Asistent Financiar BT-GO</span>
                </div>
                <button class="chat-close" id="chatClose">×</button>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message assistant">
                    <div>Salut! Sunt asistentul tău financiar virtual. Te pot ajuta cu:</div>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Analize EBITDA și sfaturi de îmbunătățire</li>
                        <li>Evaluarea rating-ului de credit</li>
                        <li>Optimizarea fluxului de numerar</li>
                        <li>Strategii de investiții și dezvoltare</li>
                        <li>Gestionarea bugetului corporativ</li>
                    </ul>
                    <div>Cum te pot ajuta astăzi?</div>
                </div>
            </div>

            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>

            <div class="chat-input-container">
                <div class="quick-suggestions">
                    <button class="suggestion-btn" data-message="Calculează EBITDA pentru compania mea">EBITDA</button>
                    <button class="suggestion-btn" data-message="Calculează rating-ul companiei">Rating</button>
                    <button class="suggestion-btn" data-message="Cum optimizez fluxul de numerar?">Cash Flow</button>
                    <button class="suggestion-btn" data-message="Strategii de investiții pentru compania mea">Investiții</button>
                </div>
                
                <div class="chat-input-wrapper">
                    <textarea 
                        class="chat-input" 
                        id="chatInput" 
                        placeholder="Scrie-mi o întrebare despre finanțele companiei..."
                        rows="1"
                    ></textarea>
                    <button class="chat-send" id="chatSend">
                        <span>➤</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        class BTGoFrontend {
            constructor() {
                this.assistantApiUrl = '';
                this.reportsApiUrl = '';
                this.isOpen = false;
                this.isTyping = false;
                this.configPanelOpen = false;
                
                this.initializeElements();
                this.attachEventListeners();
                this.loadSavedConfig();
                this.checkConnections();
            }

            initializeElements() {
                this.configToggle = document.getElementById('configToggle');
                this.configPanel = document.getElementById('configPanel');
                this.assistantUrlInput = document.getElementById('assistantUrl');
                this.reportsUrlInput = document.getElementById('reportsUrl');
                this.assistantStatus = document.getElementById('assistantStatus');
                this.reportsStatus = document.getElementById('reportsStatus');
                this.assistantStatusText = document.getElementById('assistantStatusText');
                this.reportsStatusText = document.getElementById('reportsStatusText');
                
                this.assistantBtn = document.getElementById('assistantBtn');
                this.chatOverlay = document.getElementById('chatOverlay');
                this.chatContainer = document.getElementById('chatContainer');
                this.chatClose = document.getElementById('chatClose');
                this.chatMessages = document.getElementById('chatMessages');
                this.chatInput = document.getElementById('chatInput');
                this.chatSend = document.getElementById('chatSend');
                this.typingIndicator = document.getElementById('typingIndicator');
                
                this.reportsBtn = document.getElementById('reportsBtn');
            }

            attachEventListeners() {
                this.configToggle.addEventListener('click', () => this.toggleConfigPanel());
                
                this.assistantUrlInput.addEventListener('input', () => this.saveAndUpdateConfig());
                this.reportsUrlInput.addEventListener('input', () => this.saveAndUpdateConfig());
                
                this.assistantBtn.addEventListener('click', () => this.toggleChat());
                this.chatClose.addEventListener('click', () => this.closeChat());
                this.chatOverlay.addEventListener('click', (e) => {
                    if (e.target === this.chatOverlay) this.closeChat();
                });

                this.chatSend.addEventListener('click', () => this.sendMessage());
                this.chatInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.sendMessage();
                    }
                });

                this.chatInput.addEventListener('input', this.autoResize.bind(this));

                document.querySelectorAll('.suggestion-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const message = btn.getAttribute('data-message');
                        this.chatInput.value = message;
                        this.sendMessage();
                    });
                });

                this.reportsBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.openReports();
                });

                document.addEventListener('click', (e) => {
                    if (!this.configPanel.contains(e.target) && !this.configToggle.contains(e.target)) {
                        this.closeConfigPanel();
                    }
                });
            }

            toggleConfigPanel() {
                this.configPanelOpen = !this.configPanelOpen;
                this.configPanel.classList.toggle('active', this.configPanelOpen);
            }

            closeConfigPanel() {
                this.configPanelOpen = false;
                this.configPanel.classList.remove('active');
            }

            saveAndUpdateConfig() {
                this.assistantApiUrl = this.assistantUrlInput.value;
                this.reportsApiUrl = this.reportsUrlInput.value;
                
                localStorage.setItem('btgo_assistant_url', this.assistantApiUrl);
                localStorage.setItem('btgo_reports_url', this.reportsApiUrl);
                
                this.checkConnections();
            }

            loadSavedConfig() {
                this.assistantApiUrl = localStorage.getItem('btgo_assistant_url') || '';
                this.reportsApiUrl = localStorage.getItem('btgo_reports_url') || '';
                
                this.assistantUrlInput.value = this.assistantApiUrl;
                this.reportsUrlInput.value = this.reportsApiUrl;
            }

            async checkConnections() {
                await this.checkAssistantConnection();
                await this.checkReportsConnection();
            }

            async checkAssistantConnection() {
                if (!this.assistantApiUrl) {
                    this.updateConnectionStatus('assistant', false, 'URL not set');
                    return;
                }

                try {
                    const response = await fetch(`${this.assistantApiUrl}/api/analysis`);
                    if (response.ok) {
                        this.updateConnectionStatus('assistant', true, 'Online');
                    } else {
                        this.updateConnectionStatus('assistant', false, 'Error');
                    }
                } catch (error) {
                    this.updateConnectionStatus('assistant', false, 'Offline');
                }
            }

            async checkReportsConnection() {
                if (!this.reportsApiUrl) {
                    this.updateConnectionStatus('reports', false, 'URL not set');
                    return;
                }

                try {
                    const response = await fetch(`${this.reportsApiUrl}/api/reports/health`);
                    if (response.ok) {
                        this.updateConnectionStatus('reports', true, 'Online');
                    } else {
                        this.updateConnectionStatus('reports', false, 'Error');
                    }
                } catch (error) {
                    this.updateConnectionStatus('reports', false, 'Offline');
                }
            }

            updateConnectionStatus(service, isOnline, statusText) {
                const statusIndicator = service === 'assistant' ? this.assistantStatus : this.reportsStatus;
                const statusTextElement = service === 'assistant' ? this.assistantStatusText : this.reportsStatusText;
                
                statusIndicator.classList.toggle('online', isOnline);
                statusTextElement.textContent = statusText;

                if (service === 'assistant') {
                    document.querySelector('.assistant-status').style.background = isOnline ? '#10b981' : '#f59e0b';
                }
            }

            toggleChat() {
                if (this.isOpen) {
                    this.closeChat();
                } else {
                    this.openChat();
                }
            }

            openChat() {
                this.isOpen = true;
                this.chatOverlay.classList.add('active');
                this.chatContainer.classList.add('active');
                this.chatInput.focus();
            }

            closeChat() {
                this.isOpen = false;
                this.chatOverlay.classList.remove('active');
                this.chatContainer.classList.remove('active');
            }

            openReports() {
                if (this.reportsApiUrl) {
                    window.open(this.reportsApiUrl, '_blank');
                } else {
                    this.showNotification('⚠️ Configurează URL-ul pentru Reports API', 'warning');
                    this.toggleConfigPanel();
                }
            }

            autoResize() {
                this.chatInput.style.height = 'auto';
                this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 100) + 'px';
            }

            async sendMessage() {
                const message = this.chatInput.value.trim();
                if (!message || this.isTyping) return;

                if (!this.assistantApiUrl) {
                    this.showNotification('⚠️ Configurează URL-ul pentru Assistant API', 'warning');
                    this.toggleConfigPanel();
                    return;
                }

                this.addMessage(message, 'user');
                this.chatInput.value = '';
                this.autoResize();
                this.showTyping(true);

                try {
                    const response = await fetch(`${this.assistantApiUrl}/api/chat`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        setTimeout(() => {
                            this.showTyping(false);
                            this.addAssistantMessage(data.response, data.tips);
                        }, 1000);
                    } else {
                        throw new Error('Server error');
                    }
                } catch (error) {
                    setTimeout(() => {
                        this.showTyping(false);
                        this.addOfflineResponse();
                    }, 1000);
                }
            }

            addMessage(text, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                if (Array.isArray(text)) {
                    messageDiv.innerHTML = text.map(line => `<div>${line}</div>`).join('');
                } else {
                    messageDiv.textContent = text;
                }

                this.chatMessages.appendChild(messageDiv);
                this.scrollToBottom();
            }

            addAssistantMessage(response, tips) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message assistant';
                
                let content = '';
                if (Array.isArray(response)) {
                    content = response.map(line => `<div>${line}</div>`).join('');
                } else {
                    content = `<div>${response}</div>`;
                }

                if (tips && tips.length > 0) {
                    content += '<div class="tips"><strong>💡 Sfaturi:</strong><ul>';
                    tips.forEach(tip => {
                        content += `<li>${tip}</li>`;
                    });
                    content += '</ul></div>';
                }

                messageDiv.innerHTML = content;
                this.chatMessages.appendChild(messageDiv);
                this.scrollToBottom();
            }

            addOfflineResponse() {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message assistant';
                messageDiv.innerHTML = `
                    <div>⚠️ Nu pot să mă conectez la serverul de asistență.</div>
                    <div style="margin-top: 10px;">Verifică configurarea API-ului sau încearcă din nou mai târziu.</div>
                    <div style="margin-top: 10px;">Poți să mă întrebi despre:</div>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Calcularea EBITDA</li>
                        <li>Strategii de investiții</li>
                        <li>Optimizarea cash flow-ului</li>
                        <li>Analiza ratiilor financiare</li>
                    </ul>
                `;
                this.chatMessages.appendChild(messageDiv);
                this.scrollToBottom();
            }

            showTyping(show) {
                this.isTyping = show;
                this.typingIndicator.style.display = show ? 'block' : 'none';
                this.chatSend.disabled = show;
                
                if (show) {
                    this.scrollToBottom();
                }
            }

            scrollToBottom() {
                setTimeout(() => {
                    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
                }, 100);
            }

            showNotification(message, type = 'info') {
                const notification = document.createElement('div');
                notification.style.cssText = `
                    position: fixed;
                    top: 120px;
                    right: 30px;
                    background: white;
                    padding: 15px 20px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                    border-left: 4px solid ${type === 'warning' ? '#f59e0b' : '#3b82f6'};
                    z-index: 2000;
                    opacity: 0;
                    transform: translateX(100%);
                    transition: all 0.3s ease;
                    max-width: 300px;
                    font-size: 0.9rem;
                    color: #374151;
                `;
                
                notification.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem;">${type === 'warning' ? '⚠️' : 'ℹ️'}</span>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.opacity = '1';
                    notification.style.transform = 'translateX(0)';
                }, 100);
                
                setTimeout(() => {
                    notification.style.opacity = '0';
                    notification.style.transform = 'translateX(100%)';
                    setTimeout(() => notification.remove(), 300);
                }, 4000);
            }
        }

        const btgoApp = new BTGoFrontend();

        document.addEventListener('DOMContentLoaded', function() {
            setInterval(() => {
                btgoApp.checkConnections();
            }, 30000);
        });

        console.log('🏦 BT-GO Frontend loaded successfully!');
        console.log('🚀 Configure API endpoints using the settings panel');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({'status': 'online', 'service': 'BT-GO Frontend'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)-label">Cont Curent Principal</div>
                        <div class="balance-amount">247,856.45 RON</div>
                        <div class="balance-change positive">+12,340 RON (5.2%)</div>
                    </div>
                    <div class="balance-card">
                        <div class="balance
