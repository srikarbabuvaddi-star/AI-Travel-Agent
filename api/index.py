from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import datetime

from template import INDEX_HTML

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        if "/api/plan" in path:
            try:
                from agent import TravelAgentEngine
                destination = params.get("destination", ["Goa"])[0]
                starting_city = params.get("starting_city", ["Hyderabad"])[0]
                num_people = int(params.get("num_people", ["4"])[0])
                budget = float(params.get("budget", ["40000"])[0])
                travel_style = params.get("travel_style", ["Moderate"])[0]
                food_pref = params.get("food_pref", ["Seafood"])[0]

                inputs = {
                    "destination": destination,
                    "starting_city": starting_city,
                    "start_date": str(datetime.date.today() + datetime.timedelta(days=7)),
                    "end_date": str(datetime.date.today() + datetime.timedelta(days=11)),
                    "num_people": num_people,
                    "budget": budget,
                    "trip_type": "Friends",
                    "travel_style": travel_style,
                    "food_pref": food_pref,
                    "interests": ["Beaches", "Culture", "Food"]
                }

                plan = TravelAgentEngine().plan_complete_trip(inputs)
                body = json.dumps(plan).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(body)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        # Main Single Page Application Route (Instant load from template)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(INDEX_HTML.encode('utf-8'))

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(length)

        if "/api/optimize" in path:
            try:
                from services.optimizer import optimize_trip_budget
                plan = json.loads(raw_body)
                opt = optimize_trip_budget(plan)
                res_body = json.dumps(opt).encode('utf-8')
            except Exception as e:
                res_body = json.dumps({"error": str(e)}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_body)
            return

        elif "/api/adapt" in path:
            try:
                from agent import TravelAgentEngine
                req = json.loads(raw_body)
                updated = TravelAgentEngine().adapt_itinerary(req.get("plan", {}), req.get("prompt", ""))
                res_body = json.dumps(updated).encode('utf-8')
            except Exception as e:
                res_body = json.dumps({"error": str(e)}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_body)
            return

        elif "/api/chat" in path:
            try:
                from agent import TravelAgentEngine
                req = json.loads(raw_body)
                answer = TravelAgentEngine().chat_with_trip(req.get("plan", {}), req.get("question", ""))
                res_body = json.dumps({"answer": answer}).encode('utf-8')
            except Exception as e:
                res_body = json.dumps({"answer": "How can I help with your trip details?"}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_body)
            return
