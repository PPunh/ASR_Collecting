# coding=utf-8
from django.core.management.base import BaseCommand
from apps.common.models import ProvinceModel, DistrictModel


class Command(BaseCommand):
    help = "Seed Lao Provinces and Districts data into database"

    def handle(self, *args, **kwargs):
        data = {
            "Vientiane Capital": ["Chanthabuly", "Sikhottabong", "Xaysetha", "Sisattanak", "Naxaithong", "Xaythany", "Hadxaifong", "Sangthong", "Mayparkngum"],
            "Luangprabang": ["Louangphrabang", "Xieng Ngeun", "Nan", "Park Ou", "Nambak", "Ngoi", "Pak Xeng", "Phonxay", "Chomphet", "Viengkham", "Phoukhoune"],
            "Champasak": ["Pakse", "Sanasomboon", "Bachiangchaleunsook", "Paksong", "Pathoomphone", "Phonthong", "Champassack", "Sukhuma", "Moonlapamok", "Khong"],
            "Phongsaly": ["Phongsaly", "May", "Khua", "Samphanh", "Boon Neua", "Nhot Ou", "Boontai"],
            "Luangnamtha": ["Namtha", "Sing", "Long", "Viengphoukha", "Nalae"],
            "Borkeo": ["Houixai", "Tonpheung", "Meung", "Pha Oudom", "Paktha", "Nam You"],
            "Oudomxay": ["Xay", "La", "Namor", "Nga", "Beng", "Hoon", "Pakbeng"],
            "Xayaburi": ["Xayabury", "Khop", "Hongsa", "Ngeun", "Xienghone", "Phiang", "Parklai", "Kenethao", "Xaisathan", "Botene", "Thongmyxay"],
            "Houaphan": ["Xamneua", "Xiengkhor", "Viengthong", "Viengxay", "Huameuang", "Xamtay", "Sop Bao", "Muang Et", "Kuan"],
            "Xiangkhouang": ["Pek", "Kham", "Nonghed", "Khoune", "Morkmay", "Phookood", "Phaxay", "Thathom"],
            "Vientiane Province": ["Phonhong", "Thoulakhom", "Keo Oudom", "Kasy", "Vangvieng", "Feuang", "Xanakharm", "Mad", "Hinhurp", "Viengkham"],
            "Xaisomboun": ["Anouvong", "Longchaeng", "Longxan", "Hom", "Thathom"],
            "Borlikhamxai": ["Paksane", "Thaphabath", "Pakkading", "Bolikhanh", "Khamkheuth", "Viengthong", "Xaychamphone"],
            "Khammouan": ["Thakhek", "Mahaxay", "Nongbok", "Hinboon", "Nhommalath", "Bualapha", "Nakai", "Xebangfay", "Xaybuathong"],
            "Salavan": ["Saravane", "Ta Oi", "Toomlarn", "Lakhonepheng", "Vapy", "Khongxedone", "Lao Ngarm", "Samuoi"],
            "Sekong": ["Lamarm", "Kaleum", "Dakcheung", "Thateng"],
            "Attapeu": ["Samakkhixay", "Xaysetha", "Sanamxay", "Sanxay", "Phouvong"],
            "Savannakhet": ["Khanthabouly", "Outhoomphone", "Atsaphangthong", "Phine", "Sepone", "Nong", "Thapangthong",
                            "Songkhone", "Champhone", "Xonbuly", "Xaybuly", "Vilabuly", "Atsaphone", "Xayphoothong", "Thaphalanxay"]
        }

        total_provinces = 0
        total_districts = 0

        for province_name, districts in data.items():
            province_obj, p_created = ProvinceModel.objects.get_or_create(
                name=province_name
            )
            if p_created:
                total_provinces += 1

            for district_name in districts:
                _, d_created = DistrictModel.objects.get_or_create(
                    province=province_obj,
                    name=district_name
                )
                if d_created:
                    total_districts += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database!\n"
                f"- Provinces added: {total_provinces}\n"
                f"- Districts added: {total_districts}"
            )
        )