class Converter:

    def __init__(self):
        self.months = {
            "01": "Jan", 
            "02": "Feb", 
            "03": "Mar", 
            "04": "Apr",
            "05": "May", 
            "06": "Jun", 
            "07": "Jul", 
            "08": "Aug", 
            "09": "Sep", 
            "10": "Oct",
            "11": "Nov", 
            "12": "Dec"
        }

        self.days = {
            "01": 1, 
            "02": 2, 
            "03": 3,
            "04": 4, 
            "05": 5, 
            "06": 6, 
            "07": 7, 
            "08": 8, 
            "09": 9, 
            "10": 10, 
            "11": 11,
            "12": 12, 
            "13": 13, 
            "14": 14, 
            "15": 15, 
            "16": 16, 
            "17": 17, 
            "18": 18, 
            "19": 19, 
            "20": 20, 
            "21": 21, 
            "22": 22, 
            "23": 23, 
            "24": 24, 
            "25": 25, 
            "26": 26, 
            "27": 27, 
            "28": 28, 
            "29": 29, 
            "30": 30, 
            "31": 31
        }

    def convert_date(self, date):
        day = self.days.get(date[0:2])
        month = self.months.get(date[2:4])   
        year = date[4:8]
        date_list = [day, month, year]
        return date_list

# TEST
x = Converter()
x.convert_date("02032004")


