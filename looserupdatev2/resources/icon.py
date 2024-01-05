import random


class Icon:
    bot_profile="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/looserupdatev2-icon.png"
    bot_error="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/looserupdatev2-error.png"

    ux_check="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-check-over.png"
    ux_x="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-x-over.png"
    ux_edit="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-edit-over.png"
    ux_menu="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-menu.png"
    ux_add="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-add-friend.png"
    ux_remove="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/icon-remove-friend.png"
    ux_search="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/search-icon.png"

    poro_happy="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_happy.png"
    poro_question="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_question.png"
    poro_sad="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_sad.png"
    poro_shocked="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_shocked.png"
    poro_sleeping="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_sleeping.png"
    poro_smile="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/ux/poro/poro_smile.png"

    cherry_victory="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-ch-victory.png"
    cherry_defeat="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-ch-defeat.png"
    aram_victory="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-ha-victory-v2.png"
    aram_defeat="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-ha-defeat-v2.png"
    classic_victory="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-sr-victory-v2.png"
    classic_defeat="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-sr-defeat-v2.png"
    rgm_victory="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-rgm-victory-v2.png"
    rgm_defeat="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/gamemode/icon-rgm-defeat-v2.png"

    bresil="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/br.jpg"
    europe_north_east="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/eune.jpg"
    europe_west="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/euw.jpg"
    japan="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/jp.jpg"
    latin_america_north="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/latamn.jpg"
    latin_america_south="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/latams.jpg"
    north_america="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/na.jpg"
    oceania="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/oce.jpg"
    russia="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/ru.jpg"
    turkey="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/tr.jpg"
    transfer="https://github.com/jschmittlin/looserupdatev2/blob/main/looserupdatev2/resources/assets/region/transfer.jpg"

    @classmethod
    def random_poro(cls, happy: bool = True) -> "Icon":
        happy_list = [cls.poro_happy, cls.poro_smile, cls.poro_sleeping, cls.poro_question]
        sad_list = [cls.poro_sad, cls.poro_shocked, cls.poro_sleeping, cls.poro_question]
        return random.choice(happy_list if happy else sad_list)
