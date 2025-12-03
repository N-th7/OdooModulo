from odoo import http
from odoo.http import request

class SurveyStatsController(http.Controller):

    @http.route('/internet_survey/stats', type='json', auth='user')
    def stats(self):
        surveys = request.env['internet.survey'].sudo().search([])

        SATISFACTION_MAP = {
            'muy_satisfecho': 5,
            'satisfecho': 4,
            'neutral': 3,
            'insatisfecho': 2,
            'muy_insatisfecho': 1,
        }

        numeric_values = [
            SATISFACTION_MAP.get(s.satisfaction_level, 0)
            for s in surveys
        ]

        total = len(numeric_values)
        avg = sum(numeric_values) / total if total else 0

        positive = len([v for v in numeric_values if v >= 4])
        negative = len([v for v in numeric_values if v <= 2])

        recommended = len(surveys.filtered(lambda s: s.recomedation_likelihood in [
            'definitivamente_si', 'probablemente_si'
        ]))

        recommendation_rate = (recommended * 100 / total) if total else 0

        return {
            "avg_satisfaction": round(avg, 1),
            "positive": positive,
            "negative": negative,
            "recommendation_rate": round(recommendation_rate, 1),
        }
