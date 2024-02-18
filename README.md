## What problem is the product aimed at solving?
Check air quality in selected Area. Able to see past result requested by others.

## Who is the product geared towards (targeted audience)?
People who care about air quality and also curious of which area air quality is most concerned

## How is my product unique?
It's not. But since you can see what others search for, it might give you an idea of how people care about that particular area air quality


## High-level Architecture
![](/docs/high_level.png)
- Frontend: Static Vite WebApps - A convinient UI to interact with backend. Come with pretty Chart.
- Backend: FastApi - Process to interact with database and also execute ETL process
- Database: Postgres - A popular database choice. Can't go wrong with this for small to medium data volume.
- Messaging Queue: RabbitMQ - ETL process will take unbound time to complete, decouple it from normal backend process is a good idea. Also, it's now possible to distribute the job to different ETL process.
- ETL Process: another backend process, but this will not be accessible to public. Its purpose is to query datasource with confidential API token (hence the need to be hidden from public).

## Changelog
- v0.1: Minimum Viable Product with all functionalities
- v0.2 (planned): richer visualization and explainations