# Product Overview

## What problem is the product aimed at solving?
The product aims to address the need for monitoring air quality in a specific area. Users can not only check the current air quality but also access historical data requested by others.

## Who is the product geared towards (targeted audience)?
The product is designed for individuals who are concerned about air quality and are curious about the air quality levels in different areas.

## How is my product unique?
While the product may not be unique in its core functionality, it stands out by allowing users to see what others are searching for. This feature provides insights into the areas where people are most concerned about air quality.

## High-level Architecture
![](/docs/high_level.png)
- **Frontend**: Utilizes Static Vite WebApps with an intuitive UI for interacting with the backend. It includes visually appealing charts.
- **Backend**: Powered by FastApi, the backend handles interactions with the database and executes the Extract, Transform, Load (ETL) process.
- **Database**: Relies on Postgres, a popular choice suitable for small to medium data volumes.
- **Messaging Queue**: Incorporates RabbitMQ to decouple the time-consuming ETL process from normal backend operations. This also enables job distribution across different ETL processes.
- **ETL Process**: Another backend process, not accessible to the public. Its primary function is to query the datasource using a confidential API token, ensuring it remains hidden from public view.

# Release Updates

## Changelog
- **v0.1**: Initial release with all essential functionalities.
- **v0.2 (planned)**: Upcoming release featuring enhanced visualizations and explanations.