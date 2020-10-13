{
    "name": "Pengajuan Dana dan Reimberse",
    "version": "0.1",
    "author": "richard.angga51@gmail.com",
    "category": "Extra Tools",
    "website": "My Company",
    "license": "AGPL-3",
    "summary": "",
    "description": """
   * Ajuan dana (Uang Untuk Dipertanggungjawabkan/UUDP)
   * Reimbersement
   * Pencairan dana / reimberse
   * Penyelesaian / pertanggungjawaban dana
   * Tidak ada jurnal terkait bank / cash
""",
    "depends": ["analytic",
                "account",
                "hr",
                "product",
                "purchase",
                "sale",
                "hr_expense",
                "vit_budget",
                "om_account_accountant",
                "vit_efaktur",
                "vit_efaktur_prefix"],
    "data":[
        "security/uudp_sequence.xml",
        # "security/group.xml",
        "views/uudp.xml",
        "views/template.xml",
        "security/ir.model.access.csv",
        ],
    "demo": [],
    "qweb": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}