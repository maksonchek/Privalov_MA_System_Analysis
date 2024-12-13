import json

def calculate_membership(value, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            return y1 if value == x1 else y2
    return 0.0

def task(temperature_json, heating_json, rules_json, current_temperature):
    temperature_data = json.loads(temperature_json)['температура']
    heating_data = json.loads(heating_json)['температура']
    rules = json.loads(rules_json)

    temperature_membership = {}
    for term in temperature_data:
        term_id = term['id']
        points = term['points']
        temperature_membership[term_id] = calculate_membership(current_temperature, points)

    heating_terms = {}
    for term in heating_data:
        term_id = term['id']
        points = term['points']
        heating_terms[term_id] = points

    heating_values = []
    for rule in rules:
        temp_term, heating_term = rule
        temp_membership = temperature_membership.get(temp_term, 0.0)
        heating_values.append((heating_term, temp_membership))

    max_output = 0.0
    for heating_term, weight in heating_values:
        if weight > 0:
            points = heating_terms[heating_term]
            max_value = max(x for x, _ in points)
            max_output = max(max_output, max_value * weight)

    return max_output

temperature_json = '''{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [0,0],
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}'''

heating_json = '''{
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}'''

rules_json = '''[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]'''

current_temperature = 20

optimal_control = task(temperature_json, heating_json, rules_json, current_temperature)
print(f"Оптимальное управление: {optimal_control}")
