import os
import streamlit as st

from hash_utils import calculate_sha256

from database import (
    create_table,
    register_file,
    get_registered_files,
    update_file_status,
    add_activity_log,
    get_activity_logs,
    get_scan_history,
    unregister_file
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD PROFESSIONAL CSS
# ============================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as file:

            st.html(
                f"<style>{file.read()}</style>"
            )


load_css()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_table()


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="cyber-header">

        <div class="header-left">

            <div class="shield-logo">
                🛡️
            </div>

            <div>
                <div class="main-title">
                    CyberShield
                </div>

                <div class="main-subtitle">
                    File Integrity Monitoring System
                </div>
            </div>

        </div>

        <div class="header-security">
            <span class="online-dot"></span>
            SYSTEM ONLINE
        </div>

    </div>
    """
)


# ============================================================
# SECURITY STATUS
# ============================================================

st.html(
    """
    <div class="security-banner">

        <div class="security-icon">
            🛡️
        </div>

        <div class="security-content">

            <div class="security-title">
                CyberShield Protection Active
            </div>

            <div class="security-description">
                Your registered files are protected by
                SHA-256 integrity monitoring.
            </div>

        </div>

        <div class="security-status">
            ACTIVE
        </div>

    </div>
    """
)


# ============================================================
# REFRESH DASHBOARD
# ============================================================

from datetime import datetime


refresh_col1, refresh_col2 = st.columns([6, 1])


with refresh_col1:

    if "last_refresh" not in st.session_state:

        st.session_state.last_refresh = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


    st.html(
        f"""
        <div class="refresh-info">
            🕒 Last dashboard refresh:
            <strong>{st.session_state.last_refresh}</strong>
        </div>
        """
    )


with refresh_col2:

    if st.button(
        "🔄 Refresh Dashboard",
        key="refresh_dashboard",
        use_container_width=True
    ):

        st.session_state.last_refresh = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        st.rerun()

# ============================================================
# GET REGISTERED FILES
# ============================================================

registered_files = get_registered_files()


# ============================================================
# CALCULATE STATISTICS
# ============================================================

total_files = len(registered_files)

safe_files = 0
modified_files = 0
missing_files = 0


for file_data in registered_files:

    status = file_data[5]

    if status == "Safe":

        safe_files += 1

    elif status == "Modified":

        modified_files += 1

    elif status == "Missing":

        missing_files += 1


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            📊
        </div>

        <div>
            <div class="section-title">
                Security Dashboard
            </div>

            <div class="section-description">
                Real-time overview of monitored file integrity
            </div>
        </div>

    </div>
    """
)


# ============================================================
# DASHBOARD CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


# ---------------- TOTAL ----------------

with col1:

    st.html(
        f"""
        <div class="dashboard-card total-card">

            <div class="card-top">
                <span class="card-icon">📁</span>
                <span class="card-label">TOTAL FILES</span>
            </div>

            <div class="card-value">
                {total_files}
            </div>

            <div class="card-description">
                Files under monitoring
            </div>

        </div>
        """
    )


# ---------------- SAFE ----------------

with col2:

    st.html(
        f"""
        <div class="dashboard-card safe-card">

            <div class="card-top">
                <span class="card-icon">🟢</span>
                <span class="card-label">SAFE</span>
            </div>

            <div class="card-value">
                {safe_files}
            </div>

            <div class="card-description">
                Integrity verified
            </div>

        </div>
        """
    )


# ---------------- MODIFIED ----------------

with col3:

    st.html(
        f"""
        <div class="dashboard-card modified-card">

            <div class="card-top">
                <span class="card-icon">🔴</span>
                <span class="card-label">MODIFIED</span>
            </div>

            <div class="card-value">
                {modified_files}
            </div>

            <div class="card-description">
                Changes detected
            </div>

        </div>
        """
    )


# ---------------- MISSING ----------------

with col4:

    st.html(
        f"""
        <div class="dashboard-card missing-card">

            <div class="card-top">
                <span class="card-icon">⚠️</span>
                <span class="card-label">MISSING</span>
            </div>

            <div class="card-value">
                {missing_files}
            </div>

            <div class="card-description">
                Files not found
            </div>

        </div>
        """
    )


st.divider()


# ============================================================
# REGISTER FILE
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            🔐
        </div>

        <div>
            <div class="section-title">
                Register a File
            </div>

            <div class="section-description">
                Create a SHA-256 security baseline for an important file
            </div>
        </div>

    </div>
    """
)


with st.container(border=True):

    st.write(
        "### 📁 Select File"
    )

    uploaded_file = st.file_uploader(
        "Choose a file to monitor",
        type=None,
        label_visibility="collapsed"
    )


    if uploaded_file is not None:

        st.html(
            f"""
            <div class="selected-file">

                <div class="selected-file-icon">
                    📄
                </div>

                <div>

                    <div class="selected-file-name">
                        {uploaded_file.name}
                    </div>

                    <div class="selected-file-info">
                        Ready to create security baseline
                    </div>

                </div>

            </div>
            """
        )


        if st.button(
            "🔐 Register File",
            type="primary",
            use_container_width=True
        ):

            # --------------------------------------------
            # TEMPORARY FILE
            # --------------------------------------------

            temp_file_path = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                ),
                "temp_uploaded_file"
            )


            try:

                with open(
                    temp_file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )


                # ----------------------------------------
                # CALCULATE SHA-256
                # ----------------------------------------

                file_hash = calculate_sha256(
                    temp_file_path
                )


                # ----------------------------------------
                # CREATE TEST FILES DIRECTORY
                # ----------------------------------------

                file_directory = os.path.join(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    ),
                    "test_files"
                )


                os.makedirs(
                    file_directory,
                    exist_ok=True
                )


                # ----------------------------------------
                # SAVE FILE
                # ----------------------------------------

                saved_file_path = os.path.join(
                    file_directory,
                    uploaded_file.name
                )


                with open(
                    saved_file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )


                # ----------------------------------------
                # ABSOLUTE PATH
                # ----------------------------------------

                absolute_path = os.path.abspath(
                    saved_file_path
                )


                # ----------------------------------------
                # DUPLICATE CHECK
                # ----------------------------------------

                existing_file = None


                for existing in get_registered_files():

                    if os.path.normcase(
                        os.path.abspath(
                            existing[2]
                        )
                    ) == os.path.normcase(
                        absolute_path
                    ):

                        existing_file = existing
                        break


                if existing_file is not None:

                    st.warning(
                        "⚠️ This file is already registered."
                    )

                    st.info(
                        "CyberShield did not create "
                        "a duplicate monitoring record."
                    )


                else:

                    # ------------------------------------
                    # REGISTER
                    # ------------------------------------

                    register_file(
                        uploaded_file.name,
                        absolute_path,
                        file_hash
                    )


                    # ------------------------------------
                    # ACTIVITY LOG
                    # ------------------------------------

                    add_activity_log(
                        "File Registered",
                        uploaded_file.name,
                        "Registered"
                    )


                    # ------------------------------------
                    # SUCCESS
                    # ------------------------------------

                    st.success(
                        "✅ File registered successfully!"
                    )


                    # ------------------------------------
                    # HASH DISPLAY
                    # ------------------------------------

                    st.html(
                        f"""
                        <div class="hash-panel">

                            <div class="hash-title">
                                🔐 SHA-256 Security Baseline
                            </div>

                            <div class="hash-value">
                                {file_hash}
                            </div>

                        </div>
                        """
                    )


                    st.info(
                        "This SHA-256 hash is now stored "
                        "as the security baseline."
                    )


            except Exception as error:

                st.error(
                    f"Unable to register file: {error}"
                )


            finally:

                # ----------------------------------------
                # REMOVE TEMP FILE
                # ----------------------------------------

                if os.path.exists(
                    temp_file_path
                ):

                    try:

                        os.remove(
                            temp_file_path
                        )

                    except Exception:

                        pass


st.divider()


# ============================================================
# FILE INTEGRITY SCANNER
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            🔍
        </div>

        <div>
            <div class="section-title">
                File Integrity Scanner
            </div>

            <div class="section-description">
                Compare current file hashes with their stored SHA-256 baselines
            </div>
        </div>

    </div>
    """
)


with st.container(border=True):

    st.html(
        """
        <div class="scanner-panel">

            <div class="scanner-icon">
                🔍
            </div>

            <div class="scanner-content">

                <div class="scanner-title">
                    Integrity Verification
                </div>

                <div class="scanner-description">
                    Scan every registered file and detect
                    unauthorized changes or missing files.
                </div>

            </div>

        </div>
        """
    )


    if st.button(
        "🔍 Scan All Registered Files",
        type="primary",
        use_container_width=True
    ):

        registered_files = get_registered_files()


        if not registered_files:

            st.warning(
                "⚠️ No files are registered yet."
            )


        else:

            safe_count = 0
            modified_count = 0
            missing_count = 0


            total_to_scan = len(
                registered_files
            )


            progress_bar = st.progress(
                0
            )


            status_text = st.empty()


            for index, file_data in enumerate(
                registered_files
            ):

                file_id = file_data[0]

                file_name = file_data[1]

                file_path = file_data[2]

                baseline_hash = file_data[3]


                status_text.write(
                    f"🔍 Scanning `{file_name}`..."
                )


                # ----------------------------------------
                # CHECK MISSING
                # ----------------------------------------

                if not os.path.exists(
                    file_path
                ):

                    status = "Missing"

                    missing_count += 1


                else:

                    # ------------------------------------
                    # CALCULATE CURRENT HASH
                    # ------------------------------------

                    current_hash = calculate_sha256(
                        file_path
                    )


                    # ------------------------------------
                    # COMPARE HASHES
                    # ------------------------------------

                    if current_hash == baseline_hash:

                        status = "Safe"

                        safe_count += 1

                    else:

                        status = "Modified"

                        modified_count += 1


                # ----------------------------------------
                # UPDATE DATABASE
                # ----------------------------------------

                update_file_status(
                    file_id,
                    status
                )


                # ----------------------------------------
                # ACTIVITY LOG
                # ----------------------------------------

                add_activity_log(
                    "File Integrity Scan",
                    file_name,
                    status
                )


                # ----------------------------------------
                # PROGRESS
                # ----------------------------------------

                progress_bar.progress(
                    (index + 1) / total_to_scan
                )


            status_text.success(
                "✅ Integrity scan completed successfully."
            )


            # --------------------------------------------
            # SCAN RESULTS
            # --------------------------------------------

            st.write(
                "### Scan Results"
            )


            result1, result2, result3 = st.columns(3)


            with result1:

                st.metric(
                    "🟢 Safe Files",
                    safe_count
                )


            with result2:

                st.metric(
                    "🔴 Modified Files",
                    modified_count
                )


            with result3:

                st.metric(
                    "⚠️ Missing Files",
                    missing_count
                )


st.divider()


# ============================================================
# SECURITY ACTIVITY LOG
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            📝
        </div>

        <div>
            <div class="section-title">
                Security Activity Log
            </div>

            <div class="section-description">
                Recent file registration and integrity monitoring events
            </div>
        </div>

    </div>
    """
)


activity_logs = get_activity_logs(
    20
)


if activity_logs:

    for log in activity_logs:

        log_id = log[0]

        activity = log[1]

        file_name = log[2]

        status = log[3]

        activity_time = log[4]


        if status == "Safe":

            status_class = "status-safe"
            status_text = "🟢 Safe"


        elif status == "Modified":

            status_class = "status-modified"
            status_text = "🔴 Modified"


        elif status == "Missing":

            status_class = "status-missing"
            status_text = "⚠️ Missing"


        elif status == "Registered":

            status_class = "status-registered"
            status_text = "📁 Registered"


        elif status == "Unregistered":

            status_class = "status-registered"
            status_text = "🗑️ Unregistered"


        else:

            status_class = "status-neutral"
            status_text = status


        st.html(
            f"""
            <div class="activity-card">

                <div class="activity-main">

                    <div class="activity-number">
                        #{log_id}
                    </div>

                    <div class="activity-information">

                        <div class="activity-title">
                            {activity}
                        </div>

                        <div class="activity-details">
                            📄 {file_name or "System"}
                            &nbsp;&nbsp;•&nbsp;&nbsp;
                            🕒 {activity_time}
                        </div>

                    </div>

                </div>

                <div class="{status_class}">
                    {status_text}
                </div>

            </div>
            """
        )


else:

    st.info(
        "📭 No security activities recorded yet."
    )


st.divider()


# ============================================================
# SCAN HISTORY
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            🕒
        </div>

        <div>
            <div class="section-title">
                Scan History
            </div>

            <div class="section-description">
                Previous file integrity scan results
            </div>
        </div>

    </div>
    """
)


scan_history = get_scan_history(
    50
)


if scan_history:

    for scan in scan_history:

        scan_id = scan[0]

        file_name = scan[1]

        status = scan[2]

        scan_time = scan[3]


        if status == "Safe":

            status_class = "status-safe"
            status_text = "🟢 Safe"


        elif status == "Modified":

            status_class = "status-modified"
            status_text = "🔴 Modified"


        elif status == "Missing":

            status_class = "status-missing"
            status_text = "⚠️ Missing"


        else:

            status_class = "status-neutral"
            status_text = status


        st.html(
            f"""
            <div class="history-card">

                <div class="history-left">

                    <div class="history-icon">
                        🔍
                    </div>

                    <div>

                        <div class="history-file">
                            {file_name}
                        </div>

                        <div class="history-time">
                            Scan #{scan_id}
                            &nbsp;&nbsp;•&nbsp;&nbsp;
                            🕒 {scan_time}
                        </div>

                    </div>

                </div>

                <div class="{status_class}">
                    {status_text}
                </div>

            </div>
            """
        )


else:

    st.info(
        "📭 No scan history available yet."
    )


st.divider()


# ============================================================
# REGISTERED FILES
# ============================================================

st.html(
    """
    <div class="section-heading">

        <div class="section-icon">
            📋
        </div>

        <div>
            <div class="section-title">
                Registered Files
            </div>

            <div class="section-description">
                Files currently monitored by CyberShield
            </div>
        </div>

    </div>
    """
)


registered_files = get_registered_files()


if registered_files:

    for file_data in registered_files:

        file_id = file_data[0]

        file_name = file_data[1]

        file_path = file_data[2]

        baseline_hash = file_data[3]

        registered_at = file_data[4]

        status = file_data[5]


        # --------------------------------------------
        # STATUS
        # --------------------------------------------

        if status == "Safe":

            status_class = "status-safe"
            status_text = "🟢 SAFE"


        elif status == "Modified":

            status_class = "status-modified"
            status_text = "🔴 MODIFIED"


        elif status == "Missing":

            status_class = "status-missing"
            status_text = "⚠️ MISSING"


        else:

            status_class = "status-neutral"
            status_text = status


        # --------------------------------------------
        # FILE CARD
        # --------------------------------------------

        st.html(
            f"""
            <div class="registered-file-card">

                <div class="registered-header">

                    <div class="registered-file-name">
                        📄 {file_name}
                    </div>

                    <div class="{status_class}">
                        {status_text}
                    </div>

                </div>

                <div class="file-information-grid">

                    <div class="file-information">

                        <div class="information-label">
                            FILE ID
                        </div>

                        <div class="information-value">
                            {file_id}
                        </div>

                    </div>

                    <div class="file-information">

                        <div class="information-label">
                            REGISTERED
                        </div>

                        <div class="information-value">
                            {registered_at}
                        </div>

                    </div>

                </div>

                <div class="information-label">
                    FILE PATH
                </div>

                <div class="path-value">
                    {file_path}
                </div>

                <div class="information-label">
                    SHA-256 SECURITY BASELINE
                </div>

                <div class="hash-value">
                    {baseline_hash}
                </div>

            </div>
            """
        )


        # --------------------------------------------
        # UNREGISTER
        # --------------------------------------------

        if st.button(
            "🗑️ Unregister File",
            key=f"unregister_{file_id}",
            use_container_width=True
        ):

            unregister_file(
                file_id
            )


            add_activity_log(
                "File Unregistered",
                file_name,
                "Unregistered"
            )


            st.success(
                f"✅ {file_name} was removed "
                "from CyberShield monitoring."
            )


            st.info(
                "The actual file on your computer "
                "was not deleted."
            )


            st.rerun()


else:

    st.info(
        "📭 No files are currently registered."
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="cyber-footer">

        <div class="footer-logo">
            🛡️ CyberShield
        </div>

        <div class="footer-text">
            File Integrity Monitoring System
        </div>

        <div class="footer-tech">
            Python &nbsp;•&nbsp;
            Streamlit &nbsp;•&nbsp;
            SQLite &nbsp;•&nbsp;
            SHA-256
        </div>

        <div class="footer-line">
            Security monitoring dashboard for file integrity verification.
        </div>

    </div>
    """
)