from toolkit.classifier import classify_filename


def test_common_files_are_classified_by_extension():
    assert classify_filename("acceptance_real_textbook.py")[0] == "Code"
    assert classify_filename("newstringtabs.zip")[0] == "Archives"
    assert classify_filename("ChatGPT Installer.exe")[0] == "Applications"
    assert classify_filename("acceptance-pass2.json")[0] == "Data"
    assert classify_filename("ujexa-homepage-redesign-v2.html")[0] == "Code"
    assert classify_filename("ac_circuit.cir")[0] == "Engineering Files"


def test_sensitive_names_are_flagged_before_extension_rules():
    category, reason, sensitive = classify_filename("github-recovery-codes.txt")
    assert category == "Sensitive — review"
    assert sensitive is True
    assert "excluded from AI" in reason


def test_unknown_and_extensionless_names_need_review():
    assert classify_filename("Metis v3 Acceptance Summary")[0] == "Needs review"
    assert classify_filename("archive.unknownext")[0] == "Needs review"
