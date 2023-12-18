import random


class Icon:
    bot_profile="https://cdn.discordapp.com/attachments/1039594104759271428/1186285123172311050/looserupdatev2-icon.png?ex=6592b11d&is=65803c1d&hm=94a85160cc7e8dfb8dc534df1560d03d5352a69bf1c9886eda7b5c16aaff7665&"
    bot_error="https://cdn.discordapp.com/attachments/1039594104759271428/1186285121804980254/looserupdatev2-error.png?ex=6592b11d&is=65803c1d&hm=bf1d8d8777c06e74d53fdeb624480128e51397cdf3eec3ad8e5cfeda0310474f&"

    ux_check="https://cdn.discordapp.com/attachments/1039594104759271428/1179153581618757792/icon-check-over.png?ex=6578bf59&is=65664a59&hm=0eef469f627b3b816610aea9356602e10bf8d6b815482bcfc948fcea9b4a33e4&"
    ux_x="https://cdn.discordapp.com/attachments/1039594104759271428/1179153583007088691/icon-x-over.png?ex=6578bf59&is=65664a59&hm=1175a96b4ed41a57b18e3c3e049b0f0412695348733bdaec2976901eba25e10b&"
    ux_edit="https://cdn.discordapp.com/attachments/1039594104759271428/1179153581845266452/icon-edit-over.png?ex=6578bf59&is=65664a59&hm=456014faf3d643133023e10d3e3a935d3c75a29c13dc39b640427f01613dc045&"
    ux_menu="https://cdn.discordapp.com/attachments/1039594104759271428/1179153582281465876/icon-menu.png?ex=6578bf59&is=65664a59&hm=9331d93cb01e3d5128f00001c29a7d0aeb436827174cc44868c338e5326b630a&"
    ux_add="https://cdn.discordapp.com/attachments/1039594104759271428/1180486372415524925/icon-add-friend.png?ex=657d989b&is=656b239b&hm=bb6d9c0ce897b3a6f044064ad3b3d151a10287a89751eae32d8c6c858b50d69f&"
    ux_remove="https://cdn.discordapp.com/attachments/1039594104759271428/1180486372662976572/icon-remove-friend.png?ex=657d989b&is=656b239b&hm=69a561e646f8dce0138caf3535fe7fe57c506c47cedf676edb78b232ba322f7f&"
    ux_search="https://cdn.discordapp.com/attachments/1039594104759271428/1179153583225184368/search-icon.png?ex=6578bf59&is=65664a59&hm=09c2eccc0f8ef11eb1c01a38cc280db3faa014748d138bd5039712879cc24659&"

    poro_happy="https://cdn.discordapp.com/attachments/1039594104759271428/1180486533220941864/poro_happy.png?ex=657d98c1&is=656b23c1&hm=a79ccdac02b8e711820623dfd357c2d6cbb347b2d487282801d782dce586c2e6&"
    poro_question="https://cdn.discordapp.com/attachments/1039594104759271428/1180486533795553370/poro_question.png?ex=657d98c2&is=656b23c2&hm=840f6b9f0bdaa597cc339211a981c5da2c526a52f874eeec2ba6b0e6b8bea1e3&"
    poro_sad="https://cdn.discordapp.com/attachments/1039594104759271428/1180486534261112942/poro_sad.png?ex=657d98c2&is=656b23c2&hm=a62e63713c77edfc83045ec23d0b216cab1161059143446f1c955993535e53fa&"
    poro_shocked="https://cdn.discordapp.com/attachments/1039594104759271428/1180486534563110922/poro_shocked.png?ex=657d98c2&is=656b23c2&hm=9ad5433a0a156168a5f0dcaec5c0d11272c55d8aff3259357b73e0933ad8336b&"
    poro_sleeping="https://cdn.discordapp.com/attachments/1039594104759271428/1180486534915424306/poro_sleeping.png?ex=657d98c2&is=656b23c2&hm=d2083c221cf3256403b2a315d5c07872eec64ffa7ce56b2c079ef9fba1911fe5&"
    poro_smile="https://cdn.discordapp.com/attachments/1039594104759271428/1180486535179681842/poro_smile.png?ex=657d98c2&is=656b23c2&hm=382ef244ed211c9f265b07d01ab775f0353626c2f9e8afa92b1f53a9be32d97d&"

    cherry_victory="https://cdn.discordapp.com/attachments/1039594104759271428/1179153378392146010/icon-ch-victory.png?ex=6578bf29&is=65664a29&hm=2fca1df4d184e9b77f4350349da50a6a4cf29d7e80b385dd17a84d4c50ba22f3&"
    cherry_defeat="https://cdn.discordapp.com/attachments/1039594104759271428/1179153378174046391/icon-ch-defeat.png?ex=6578bf28&is=65664a28&hm=c9ac9fd7fc55a6912e4b36c81aee14831d4c705c29a49b67f5fe6421d7030cd5&"
    aram_victory="https://cdn.discordapp.com/attachments/1039594104759271428/1179153378828357793/icon-ha-victory-v2.png?ex=6578bf29&is=65664a29&hm=ca9532b6041f30c1d4e5edab7297f96583792c836f9488fd2c93ea7067210634&"
    aram_defeat="https://cdn.discordapp.com/attachments/1039594104759271428/1179153378589290596/icon-ha-defeat-v2.png?ex=6578bf29&is=65664a29&hm=7fc690a0e0116bb84ac2ab127a53fb487befce3ce99678e3942362702910d863&"
    classic_victory="https://cdn.discordapp.com/attachments/1039594104759271428/1179153379746906122/icon-sr-victory-v2.png?ex=6578bf29&is=65664a29&hm=8e6ece751401bf7ed22112370841e91566859c6e87eb8408d0f848e85d1dad2f&"
    classic_defeat="https://cdn.discordapp.com/attachments/1039594104759271428/1179153379499446333/icon-sr-defeat-v2.png?ex=6578bf29&is=65664a29&hm=c873cc7aff4c75c868e9599450308c680e95257cc8c0df194b5f28ac07cfacc2&"
    rgm_victory="https://cdn.discordapp.com/attachments/1039594104759271428/1179153379285545030/icon-rgm-victory-v2.png?ex=6578bf29&is=65664a29&hm=4a4276406a70aa06ec583a2cae98f754178ded8cd9c5f9aca9e5b796ba05c8e4&"
    rgm_defeat="https://cdn.discordapp.com/attachments/1039594104759271428/1179153379054846122/icon-rgm-defeat-v2.png?ex=6578bf29&is=65664a29&hm=33d64afcca71c4a845c1a6b70f8c5949342043c289e5e7c3a6de92ca16b95e32&"

    bresil="https://cdn.discordapp.com/attachments/1039594104759271428/1179156268666069022/br.jpg?ex=6578c1da&is=65664cda&hm=96895860cc31a89f0a9405e946c396e3b36dd86a3c11e93248557ad6c5e7fc60&"
    europe_north_east="https://cdn.discordapp.com/attachments/1039594104759271428/1179156268909334578/eune.jpg?ex=6578c1da&is=65664cda&hm=2e234c73058fd9d889e9bc455545d15c2afc3403688dfd36043709f1588199ef&"
    europe_west="https://cdn.discordapp.com/attachments/1039594104759271428/1179156269161009263/euw.jpg?ex=6578c1da&is=65664cda&hm=b5531e3af5f7c95f20977cf143162c94cdfa9c579b222318adfb6a09dab041ec&"
    japan="https://cdn.discordapp.com/attachments/1039594104759271428/1179156269379100762/jp.jpg?ex=6578c1da&is=65664cda&hm=855bede6f4e431859db40bb0017303b0a7415babc1e70fbb3b6587b68cabb07d&"
    latin_america_north="https://cdn.discordapp.com/attachments/1039594104759271428/1179156269643337889/latamn.jpg?ex=6578c1da&is=65664cda&hm=8aa2847558716a67db26346519d53cb4aa09e96a6b9707e62e92d03aedc613f7&"
    latin_america_south="https://cdn.discordapp.com/attachments/1039594104759271428/1179156269995675658/latams.jpg?ex=6578c1da&is=65664cda&hm=5220a1102c83fbdd251a424d87170f8f96201725b15675317b611828b27a8d6e&"
    north_america="https://cdn.discordapp.com/attachments/1039594104759271428/1179156270293459055/na.jpg?ex=6578c1da&is=65664cda&hm=125cf14ff0590fb1231a996f6bafd950b29364c0e59ae699f65cbf7701b9d03f&"
    oceania="https://cdn.discordapp.com/attachments/1039594104759271428/1179156270540935238/oce.jpg?ex=6578c1da&is=65664cda&hm=797d6f0d8329d6d22c184abb11824661081e0599335516bb7cbe0ad19a86f606&"
    russia="https://cdn.discordapp.com/attachments/1039594104759271428/1179156270830329856/ru.jpg?ex=6578c1da&is=65664cda&hm=06869a32132b66ec13e74e916d32913d230dfb15fdf66ea1a8594aac79cc3f8e&"
    turkey="https://cdn.discordapp.com/attachments/1039594104759271428/1179156271585300531/tr.jpg?ex=6578c1da&is=65664cda&hm=f3918bc7a9b421bd9a897b928c4d57e61f3db7ba12411c5fa8992250b38e051c&"
    transfer="https://cdn.discordapp.com/attachments/1039594104759271428/1179156295488643072/transfer.jpg?ex=6578c1e0&is=65664ce0&hm=08c9200367954dd23ef3831470fadc3623300fd19c67b48c0c586361a7e44ed2&"

    @classmethod
    def random_poro(cls, happy: bool = True) -> "Icon":
        happy_list = [cls.poro_happy, cls.poro_smile, cls.poro_sleeping, cls.poro_question]
        sad_list = [cls.poro_sad, cls.poro_shocked, cls.poro_sleeping, cls.poro_question]
        return random.choice(happy_list if happy else sad_list)
