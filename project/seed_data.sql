USE skin_diagnosis_db;

INSERT INTO diseases (name, category, description, remedies, precautions, doctor_advice, validated) VALUES
('fungal infection', 'Fungal', 'A common skin fungal infection causing itchy ring-shaped rashes.', 'Use antifungal creams such as clotrimazole; keep skin dry.', 'Avoid sharing towels and maintain personal hygiene.', 'Consult dermatologist if no improvement in 5-7 days.', TRUE),
('bacterial dermatitis', 'Bacterial', 'Inflammatory bacterial skin condition with redness and swelling.', 'Use prescribed topical antibiotics and gentle cleansing.', 'Avoid scratching and keep area clean.', 'Seek doctor advice if pain, fever, or spreading occurs.', TRUE),
('viral rash', 'Viral', 'Rash caused by viral infection; may be contagious.', 'Supportive care, hydration, and physician-guided antivirals if needed.', 'Avoid close contact during active rash.', 'Immediate doctor consultation for fever or breathing difficulty.', TRUE),
('protozoan skin lesion', 'Protozoan', 'Lesions due to protozoal parasitic infection.', 'Requires targeted antiparasitic treatment prescribed by doctor.', 'Prevent insect bites and maintain sanitation.', 'Consult infectious disease specialist promptly.', TRUE);

INSERT INTO chatbot_knowledge (question_pattern, answer, category) VALUES
('what causes fungal infection', 'Fungal skin infections are usually caused by dermatophyte fungi that grow in warm, moist areas.', 'fungal'),
('is this contagious', 'Some skin conditions are contagious, especially fungal and viral diseases. Avoid sharing personal items.', 'general'),
('what treatment should i use', 'Treatment depends on the diagnosed condition. Please review the remedy section and consult a doctor for prescription therapy.', 'treatment'),
('can i self medicate', 'Avoid self-medication for severe or persistent symptoms. Professional diagnosis is strongly recommended.', 'safety');
