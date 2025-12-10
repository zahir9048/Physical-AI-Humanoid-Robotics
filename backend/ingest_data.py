import asyncio
import uuid
from src.services.qdrant_service import QdrantService, TextbookChunk

async def ingest_data():
    qdrant_service = QdrantService()
    
    # Dummy data representing textbook content
    chunks = [
        TextbookChunk(
            id=str(uuid.uuid4()),
            content="Physical AI integrates AI with physical systems, enabling robots to interact with the real world.",
            title="Introduction to Physical AI",
            chapter="Chapter 1",
            section="1.1",
            url="/docs/intro",
            source_file="intro.md",
            position=1
        ),
        TextbookChunk(
            id=str(uuid.uuid4()),
            content="Humanoid robotics focuses on creating robots that mimic human form and function.",
            title="Humanoid Robotics Basics",
            chapter="Chapter 2",
            section="2.1",
            url="/docs/humanoid-basics",
            source_file="humanoid.md",
            position=2
        ),
        TextbookChunk(
            id=str(uuid.uuid4()),
            content="Kinematics describes the motion of points, bodies, and systems of bodies without identifying the forces that cause the motion.",
            title="Kinematics",
            chapter="Chapter 3",
            section="3.1",
            url="/docs/kinematics",
            source_file="kinematics.md",
            position=3
        )
    ]
    
    print(f"Ingesting {len(chunks)} chunks into Qdrant...")
    success = await qdrant_service.batch_add_chunks(chunks)
    
    if success:
        print("Successfully ingested data!")
    else:
        print("Failed to ingest data.")

if __name__ == "__main__":
    asyncio.run(ingest_data())
