# clear_tables(con)
# test_inputs()

# # Example calls for delete functions
#=====================================================
# delete_user_by_username(con, ("jane_smith",))
# delete_your_kahoot_by_id(con, 1)
# delete_quiz_with_written_answer(con, 1)
# delete_quiz_answer_with_written_answer(con, 1)
# delete_quiz_with_true_false(con, 3)
#=====================================================

# # Example calls for update functions
# #=====================================================
# update_quiz_with_true_false(con, 1, "Did the catholic church believe earth was center of universe in 16th century", True, 1)
# update_quiz_answer_with_written_answer(con, 1, 1, '6')
# update_quiz_question_with_written_answer(con, 1, 'What is 3 + 3', 1)
# update_your_kahoot_by(con, 1, 'The best kahoot', 'Best of the best', True, 1)
# update_groups(con, 3, 'Teknikhögskolan', 'AI nerds')
# update_presentation_classic(con, 3, 1, title='Welcome to the Tobias AI-quiz', text='Prepare to be amazed by AI-generated questions!')
# #=====================================================

# # Example calls for patch functions
# #=====================================================
# patch_question_quiz_with_true_false(con, 1, "Do most people believe the earth is flat?")
# #=====================================================

def clear_tables(con):
    with con:
        with con.cursor() as cur:
            cur.execute("""
                TRUNCATE TABLE
                    users,
                    subscriptions,
                    languages,
                    customer_types,
                    your_kahoot,
                    kahoot_owners,
                    favorite_kahoots,
                    groups,
                    user_group_members,
                    quiz_with_written_answer,
                    quiz_written_answer,
                    quiz_with_true_false,
                    presentation_classic
                RESTART IDENTITY CASCADE
            """)
    print("All tables TRUNCATED (IDs reset to 1)!")

# # INPUTS
# # Test inputs for database creation functions

def test_inputs():
    subscriptions_tests = [
        "Premium",
        "Basic", 
        "Premium",
        "FREE-UPPERCASE",
        "  trimmed-sub  ",
    ]

    for name in subscriptions_tests:
        create_subscriptions(con, name)  # con is your actual connection variable

    # create_languages inputs
    languages_tests = [
        "English",      # → Inserts new language "English"
        "Swedish",      # → Inserts new language "Swedish"
        # "English",      # → Raises UniqueViolation (already exists)
        "sv-SE",        # → Inserts locale format "sv-SE"
        "日本語"         # → Inserts Unicode "日本語"
    ]

    for name in languages_tests:
        create_languages(con, name)

    # create_customer_types inputs
    customer_types_tests = [
        "Individual",     # → Inserts new customer type "Individual"
        "Business",       # → Inserts new customer type "Business"
        # "Individual",     # → Raises UniqueViolation (already exists)
        "B2B-Enterprise", # → Inserts "B2B-Enterprise"
        "Non-Profit"      # → Inserts "Non-Profit"
    ]

    for name in customer_types_tests:
        create_customer_types(con, name)

    # create_users inputs (assumes subscriptions_id=1, language_id=1, customer_type_id=1 exist)
    users_tests = [
        ("john_doe", "john@example.com", "hashedpass1", "1990-05-15", 1, 1, 1),  # → Creates user with no name/organisation
        ("jane_smith", "jane@test.se", "hashedpass2", "1985-12-03", 1, 1, 1, "Jane Smith"),  # → Creates with name only
        # ("test_user", "test@example.com", "pass", "2000-01-01", 999, 1, 1),  # → Raises ForeignKeyViolation (invalid subscriptions_id)
        # ("admin", "admin@company.se", "adminpass", "1970-01-01", 1, 999, 1),  # → Raises ForeignKeyViolation (invalid language_id)
        ("user5", "user5@org.com", "pass5", "1995-07-20", 1, 1, 1, "User Five", "TechCorp")  # → Creates full user with all fields
    ]

    for args in users_tests:
        create_users(con, *args)
    
        # your_kahoot
    your_kahoot_tests = [
        ("My first kahoot", 1),
        ("Swedish capitals", 1, "Quiz about Swedish geography"),
        ("Private math quiz", 1, "Algebra basics", True),
        ("No description public", 1, None, False),
    ]

    for args in your_kahoot_tests:
        create_your_kahoot(con, *args)


    # kahoot_owners
    kahoot_owners_tests = [
        (1, 1),   # user 1 → kahoot 1
        (1, 2),   # user 1 → kahoot 2
        (2, 1),   # user 2 → kahoot 1
    ]

    for users_id, your_kahoot_id in kahoot_owners_tests:
        create_kahoot_owners(con, users_id, your_kahoot_id)


    # favorite_kahoots
    favorite_kahoots_tests = [
        (1, 1),
        (1, 2),
        (2, 1),
    ]

    for users_id, your_kahoot_id in favorite_kahoots_tests:
        create_favorite_kahoots(con, users_id, your_kahoot_id)


    # groups
    groups_tests = [
        ("Teachers", "Internal teacher group"),
        ("Students", "All students in class 9A"),
        ("Empty description group", None),
        ("Special chars ✓", "Unicode test"),
    ]

    for name, description in groups_tests:
        create_groups(con, name, description)


    # user_group_members
    user_group_members_tests = [
        (1, 1),
        (1, 2),
        (2, 1),
    ]

    for user_id, group_id in user_group_members_tests:
        create_user_group_members(con, user_id, group_id)


    # written quiz
    written_quiz_tests = [
        ("What is 2+2?", 1),
        ("Capital of Sweden?", 1),
        ("Long description question...", 2),
    ]

    for question, your_kahoot_id in written_quiz_tests:
        create_written_quiz(con, question, your_kahoot_id)


    # written quiz answers
    answer_quiz_tests = [
        ("4", 1),
        ("Stockholm", 2),
        ("Wrong but valid", 1),
    ]

    for answer, quiz_with_written_answer_id in answer_quiz_tests:
        create_answer_quiz(con, answer, quiz_with_written_answer_id)


    # true/false quiz
    true_false_quiz_tests = [
        ("The earth is flat", False, 1),
        ("Stockholm is in Sweden", True, 1),
        ("Edge case question", True, 2),
    ]

    for question, answer, your_kahoot_id in true_false_quiz_tests:
        create_true_false_quiz(con, question, answer, your_kahoot_id)


    # presentation_classic
    presentation_classic_tests = [
        ("Intro slide", "Welcome to this kahoot", 1),
        ("Rules", "Answer fast to get more points", 1),
        (None, "Text-only slide", 1),
        ("Title only", None, 1),
    ]

    for title, text, your_kahoot_id in presentation_classic_tests:
        create_presentation_classic(con, your_kahoot_id, title, text)
