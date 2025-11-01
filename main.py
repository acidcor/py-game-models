import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "rb") as file:
        players = json.load(file)

    for nickname in players:
        if Player.objects.filter(nickname=nickname).exists():
            continue

        player = players[f"{nickname}"]

        if not player.get("race"):
            raise ValueError("Field 'Raise' can't be empty")

        race_name, race_description, skills = player["race"].values()

        race, _ = Race.objects.get_or_create(
            name=race_name,
            description=race_description
        )

        if skills:
            for skill in skills:
                name, bonus = skill.values()
                Skill.objects.get_or_create(
                    name=name,
                    bonus=bonus,
                    race=race
                )

        guild = player["guild"]

        if guild:
            guild_name, description = guild.values()
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                description=description
            )
        else:
            guild = None

        Player.objects.create(
            nickname=nickname,
            email=player["email"],
            bio=player["bio"],
            race=race,
            guild=guild,
        )


if __name__ == "__main__":
    main()
