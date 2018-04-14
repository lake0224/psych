"""Defined a robot model"""

from roboter.models import ranking

DEFAULT_ROBOT_NAME = 'Robotaro'

class Robot():
    """Based robot model"""
    def __init__(self, name = DEFAULT_ROBOT_NAME, user_name = ''):
        self.name = name
        self.user_name = user_name


    def hello(self):
        """Return words to the user that the robot speaks at the beginnig"""
        print('こんにちは！私は{}です。あなたの名前はなんですか？'.format(self.name))
        user_name = input()
        if user_name:
            self.user_name = user_name.title()

class RestaurantRobot(Robot):
    """Handle data model on restaurant."""

    def __init__(self, name = DEFAULT_ROBOT_NAME):
        super().__init__(name = name)
        ###ランキングデータを取得する
        self.ranking_model = ranking.RankingModel()
    def _hello_decorator(func):
        """Decorator to say a greeting if you are not greeting the user."""
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper

    @_hello_decorator
    def recommend_restaurant(self):
        """Show restaurant recommended restaurant to the user"""
        new_recommend_restaurant = self.ranking_model.get_most_popular()
        if not new_recommend_restaurant:
            return None

        will_recommend_restaurants = [new_recommend_restaurant]
        while True:
            print('私のオススメのレストランは、{}です。\nこのレストランは好きですか？ [Yes/No]'.format(new_recommend_restaurant))
            is_yes = input()

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break
            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_restaurant = self.ranking_model.get_most_popular(not_list = will_recommend_restaurants)
                if not new_recommend_restaurant:
                    break
                will_recommend_restaurants.append(new_recommend_restaurant)


    @_hello_decorator
    def ask_user_favorite(self):
        """Collect favorite restaurant information from users"""
        while True:
            print('{}さん。どこのレストランが好きですか？'.format(self.user_name))
            restaurant = input()
            if restaurant:
                self.ranking_model.increment(restaurant)
                break

    @_hello_decorator
    def thank_you(self):
        """Show words of appreciation to users."""
        print('{}さん。ありがとうございました。\nよい一日を！さようなら。'.format(self.name))







