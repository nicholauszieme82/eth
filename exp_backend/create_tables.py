from app import Base, engine
from app import models  # this is important to ensure all models are imported

Base.metadata.create_all(engine)
print("✅ Tables created!")

