from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Optimal Cluster Estimator", "goal": "Determinar K óptimo con el método del Codo y Silhouette Score."},
    {"role": "K-Means & Medoids Modeler", "goal": "Entrenar y converger particiones centroides estables."},
    {"role": "Hierarchical & DBSCAN Specialist", "goal": "Identificar clusters de densidad y detectar ruido/outliers."},
    {"role": "Cluster Profiler", "goal": "Caracterizar las medias y perfiles de comportamiento por segmento."},
    {"role": "Segment Labeler", "goal": "Asignar nombres descriptivos y personas a cada cluster de datos."},
    {"role": "Clustering Insight Synthesizer", "goal": "Resumir el valor de negocio de la segmentación."}
]

clustering_crew = create_specialized_crew("Clustering Crew", "gemini", agents)
