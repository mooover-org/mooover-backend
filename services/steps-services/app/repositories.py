from corelib.domain.errors import NotFoundError
from corelib.domain.models import User
from neo4j import Neo4jDriver, GraphDatabase

from app.config import AppConfig


class Neo4jStepsRepository:
    """Neo4J repository operations for steps"""

    driver: Neo4jDriver

    def __init__(self, driver: Neo4jDriver = GraphDatabase.driver(uri=AppConfig().neo4j_config['HOST'], auth=(
            AppConfig().neo4j_config['USER'], AppConfig().neo4j_config['PASSWORD']))) -> None:
        self.driver = driver

    def add_new_steps(self, user_id: str, steps: int) -> None:
        def _add_new_steps(tx, user_primary_key: str, number_of_steps: str):
            result = tx.run(f"MATCH (u:User {{{User.__primarykey__}: '{user_primary_key}'}}) "
                            f"RETURN u "
                            f"LIMIT 1")
            if result.single():
                tx.run(f"MATCH (u:User {{{User.__primarykey__}: '{user_primary_key}'}}) "
                       f"SET u.today_steps = u.today_steps + {number_of_steps}, "
                       f"u.this_week_steps = u.this_week_steps + {number_of_steps} "
                       f"WITH u "
                       f"MATCH (u)-[:MEMBER_OF]->(g:Group) "
                       f"SET g.today_steps = g.today_steps + {number_of_steps}, "
                       f"g.this_week_steps = u.this_week_steps + {number_of_steps} ")
            else:
                raise NotFoundError("User not found")

        with self.driver.session() as session:
            session.write_transaction(_add_new_steps, user_id, str(steps))

    def reset_all_daily_steps(self) -> None:
        def _reset_all_daily_steps(tx):
            tx.run(f"MATCH (u:User) "
                   f"SET today_steps = 0")
            tx.run(f"MATCH (g:Groups) "
                   f"SET today_steps = 0")

        with self.driver.session() as session:
            session.write_transaction(_reset_all_daily_steps)

    def reset_all_weekly_steps(self) -> None:
        def _reset_all_weekly_steps(tx):
            tx.run(f"MATCH (u:User) "
                   f"SET this_week_steps = 0")
            tx.run(f"MATCH (g:Groups) "
                   f"SET this_week_steps = 0")

        with self.driver.session() as session:
            session.write_transaction(_reset_all_weekly_steps)
