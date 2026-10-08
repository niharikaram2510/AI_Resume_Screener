import streamlit as st
import pandas as pd
import time

from ranking.resume_ranker import rank_resumes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = []

if "job_role" not in st.session_state:
    st.session_state.job_role = ""


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
    ====================================================== */

    .stApp {
        background: #f5f8fc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
        background: linear-gradient(
            180deg,
            #12376f 0%,
            #0b2c5b 100%
        );
    }

    section[data-testid="stSidebar"] > div {
        width: 250px !important;
    }

    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    .sidebar-title {
        color: #ffffff !important;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 28px;
    }

    .sidebar-section {
        color: #ffffff !important;
        font-size: 11px;
        font-weight: 800;
        margin-top: 18px;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }

    .sidebar-description {
        background: #eef5ff !important;
        color: #47617f !important;
        border-radius: 9px;
        padding: 13px;
        font-size: 11px;
        line-height: 1.55;
        margin-top: 14px;
    }

    .sidebar-small {
        color: #d8e4f4 !important;
        font-size: 11px;
        line-height: 1.8;
    }


    /* ======================================================
       PAGE HEADER
    ====================================================== */

    .page-title {
        color: #20477d !important;
        font-size: 34px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 5px;
    }

    .page-subtitle {
        color: #718096 !important;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #20477d !important;
        font-size: 23px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #718096 !important;
        font-size: 13px;
        margin-bottom: 15px;
    }


    /* ======================================================
       CARDS
    ====================================================== */

    .card {
        background: #ffffff !important;
        border: 1px solid #dce5ef;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(25, 50, 85, 0.06);
        min-height: 90px;
    }

    .card-title {
        color: #173f75 !important;
        font-size: 17px;
        font-weight: 800;
        line-height: 1.4;
        margin-bottom: 5px;
    }

    .card-subtitle {
        color: #718096 !important;
        font-size: 12px;
        line-height: 1.5;
    }


    /* ======================================================
       INPUTS
    ====================================================== */

    div[data-baseweb="input"] {
        background: #ffffff !important;
        border: 1px solid #ccd8e6 !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="input"] > div {
        background: #ffffff !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="input"] input {
        background: #ffffff !important;
        color: #26384f !important;
        -webkit-text-fill-color: #26384f !important;
        font-size: 14px !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #8a98aa !important;
        -webkit-text-fill-color: #8a98aa !important;
        opacity: 1 !important;
    }


    /* ======================================================
       FILE UPLOADER
    ====================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;
        border: 2px dashed #c8d7e8 !important;
        border-radius: 12px !important;
        padding: 18px !important;
    }

    section[data-testid="stFileUploaderDropzone"] div,
    section[data-testid="stFileUploaderDropzone"] span {
        color: #526781 !important;
    }

    section[data-testid="stFileUploaderDropzone"] button {
        background: #edf4ff !important;
        color: #245796 !important;
        border: 1px solid #d3e2f7 !important;
        border-radius: 8px !important;
    }


    /* ======================================================
       BUTTONS
    ====================================================== */

    .stButton > button {
        border-radius: 9px !important;
        min-height: 42px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: #245996 !important;
        border: none !important;
        color: #ffffff !important;
    }


    /* ======================================================
       STREAMLIT METRICS
    ====================================================== */

    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #dfe7f0 !important;
        border-radius: 13px !important;
        padding: 15px !important;
        box-shadow: 0 4px 14px rgba(25, 50, 85, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #718096 !important;
    }

    [data-testid="stMetricValue"] {
        color: #173f75 !important;
    }


    /* ======================================================
       SCORE
    ====================================================== */

    .score-number {
        color: #173f75 !important;
        font-size: 28px;
        font-weight: 800;
    }

    .score-bar-background {
        width: 100%;
        height: 9px;
        background: #e5ebf3;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 8px;
    }

    .score-bar-fill {
        height: 100%;
        background: #32a866;
        border-radius: 10px;
    }


    /* ======================================================
       CANDIDATE CARD
    ====================================================== */

    .candidate-card {
        background: #ffffff !important;
        border: 1px solid #dfe7f0;
        border-radius: 14px;
        padding: 20px;
        margin-top: 12px;
    }

    .candidate-name {
        color: #173f75 !important;
        font-size: 18px;
        font-weight: 800;
    }

    .candidate-meta {
        color: #718096 !important;
        font-size: 12px;
    }


    /* ======================================================
       SKILL CHIPS
    ====================================================== */

    .skill-chip {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }

    .matched-chip {
        background: #e4f7ec !important;
        color: #187346 !important;
    }

    .missing-chip {
        background: #fde8e8 !important;
        color: #b42323 !important;
    }


    /* ======================================================
       EXPANDERS
    ====================================================== */

    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #dfe7f0 !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary {
        color: #173f75 !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       DATAFRAME
    ====================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #dfe7f0;
        border-radius: 10px;
    }


    /* ======================================================
       ALERTS
    ====================================================== */

    div[data-testid="stAlert"] {
        color: #26384f !important;
    }

    div[data-testid="stAlert"] p {
        color: #26384f !important;
    }


    /* ======================================================
       FOOTER
    ====================================================== */

    .footer {
        text-align: center;
        color: #8a98aa !important;
        font-size: 11px;
        padding: 35px 0 10px;
    }


    /* ======================================================
       RESPONSIVE
    ====================================================== */

    @media (max-width: 1000px) {

        section[data-testid="stSidebar"] {
            width: 220px !important;
            min-width: 220px !important;
        }

        section[data-testid="stSidebar"] > div {
            width: 220px !important;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .page-title {
            font-size: 29px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📄 AI Resume Screener</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">SCREENING</div>',
        unsafe_allow_html=True
    )

    sidebar_role = st.text_input(
        "Job Role",
        placeholder="e.g. Machine Learning Engineer",
        value=st.session_state.job_role,
        key="sidebar_role"
    )

    st.session_state.job_role = sidebar_role

    st.markdown(
        """
        <div class="sidebar-description">
            Enter a job role in natural language.
            The system maps it to the closest role
            from the 50-role knowledge base using
            MiniLM semantic similarity.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">SUPPORTED FORMATS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-small">
            ✓ PDF resumes<br>
            ✓ DOCX resumes<br>
            ✓ Multiple candidates<br>
            ✓ AI-based ranking
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-small">
            <b>Deep Learning Resume Screening System</b>
            <br><br>
            MiniLM Semantic Matching<br>
            DistilBERT Resume-NER
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="page-title">AI Resume Screening</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="page-subtitle">
        Upload multiple resumes and find the best
        candidates for your selected job using AI.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP SECTION
# ============================================================

upload_col, config_col, stats_col = st.columns(
    [1.35, 1.35, 0.55],
    gap="medium"
)


# ============================================================
# UPLOAD RESUMES
# ============================================================

with upload_col:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                1. Upload Resumes
            </div>
            <div class="card-subtitle">
                Upload PDF or DOCX files (multiple allowed)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload candidate resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    st.caption(
        "Supported formats: PDF, DOCX • Maximum 10 files"
    )


# ============================================================
# SCREENING CONFIGURATION
# ============================================================

with config_col:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                2. Screening Configuration
            </div>
            <div class="card-subtitle">
                Review the selected screening role.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_role = st.session_state.job_role

    if selected_role.strip():

        st.markdown(
            """
            <div style="
                margin-top:15px;
                margin-bottom:8px;
                color:#405875;
                font-size:12px;
                font-weight:700;
            ">
                Screening Role
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(selected_role)

    else:

        st.warning(
            "Enter a job role in the left sidebar to begin screening."
        )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    analyze_clicked = st.button(
        "🔍  Analyze Resumes",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# QUICK STATS
# ============================================================

with stats_col:

    uploaded_count = (
        len(uploaded_files)
        if uploaded_files
        else 0
    )

    processed_count = len(
        st.session_state.results
    )

    st.metric(
        "📄 Uploaded",
        uploaded_count
    )

    st.metric(
        "✓ Processed",
        processed_count
    )


# ============================================================
# ANALYZE RESUMES
# ============================================================

if analyze_clicked:

    if not st.session_state.job_role.strip():

        st.error(
            "Please enter a job role in the left sidebar."
        )

    elif not uploaded_files:

        st.error(
            "Please upload at least one resume."
        )

    elif len(uploaded_files) > 10:

        st.error(
            "Please upload a maximum of 10 resumes."
        )

    else:

        progress = st.progress(
            0,
            text="Preparing resume analysis..."
        )

        start_time = time.time()

        try:

            progress.progress(
                20,
                text="Extracting resume information..."
            )

            # No Job Description is passed.
            # Only the selected role and resumes are used.

            results = rank_resumes(
                uploaded_files,
                st.session_state.job_role
            )

            progress.progress(
                70,
                text="Running AI skill and semantic analysis..."
            )

            time.sleep(0.2)

            progress.progress(
                100,
                text="Screening completed."
            )

            time.sleep(0.3)

            progress.empty()

            st.session_state.results = results

            elapsed = round(
                time.time() - start_time,
                2
            )

            st.success(
                f"Successfully screened "
                f"{len(uploaded_files)} resume(s) "
                f"in {elapsed} seconds."
            )

        except Exception as error:

            progress.empty()

            st.error(
                f"Screening failed: {error}"
            )


# ============================================================
# RESULTS
# ============================================================

results = st.session_state.results


if results:

    valid_results = [
        result
        for result in results
        if "error" not in result
    ]

    failed_results = [
        result
        for result in results
        if "error" in result
    ]


    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.markdown(
        '<div class="section-title">Candidate Ranking Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Candidates ranked using semantic role matching,
            Transformer-based resume understanding and
            skill matching.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    if valid_results:

        top_candidate = valid_results[0]

        stat1, stat2, stat3, stat4 = st.columns(
            4,
            gap="medium"
        )

        with stat1:

            st.metric(
                "Candidates Screened",
                len(valid_results)
            )

        with stat2:

            st.metric(
                "Top Candidate",
                top_candidate["candidate"]
            )

        with stat3:

            st.metric(
                "Top Score",
                f'{top_candidate["overall_score"]}%'
            )

        with stat4:

            st.metric(
                "Matched Role",
                top_candidate["matched_role"]
            )


    # ========================================================
    # RANKING TABLE
    # ========================================================

    if valid_results:

        st.markdown(
            '<div class="section-title">Ranking</div>',
            unsafe_allow_html=True
        )

        table_data = []

        for result in valid_results:

            table_data.append(
                {
                    "Rank": result["rank"],
                    "Candidate": result["candidate"],
                    "Matched Role": result["matched_role"],
                    "Overall Score": f'{result["overall_score"]}%',
                    "Skill Match": f'{result["skill_score"]}%',
                    "Experience": f'{result["experience_score"]}%',
                    "Projects": f'{result["project_score"]}%',
                    "Career Stage": result["career_stage"]
                }
            )

        ranking_df = pd.DataFrame(
            table_data
        )

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        csv_data = ranking_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Ranking Results",
            data=csv_data,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )


    # ========================================================
    # CANDIDATE DETAILS
    # ========================================================

    if valid_results:

        st.markdown(
            '<div class="section-title">Candidate Details</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-subtitle">
                Detailed AI screening analysis for each candidate.
            </div>
            """,
            unsafe_allow_html=True
        )


        for result in valid_results:

            candidate = result["candidate"]
            score = result["overall_score"]
            rank = result["rank"]

            with st.expander(
                f'#{rank}  {candidate}  —  {score}%'
            ):

                # --------------------------------------------
                # CANDIDATE HEADER
                # --------------------------------------------

                clean_name = (
                    candidate
                    .replace(".pdf", "")
                    .replace(".docx", "")
                    .replace("_", " ")
                )

                words = clean_name.split()

                initials = "".join(
                    word[0]
                    for word in words
                    if word
                )[:2].upper()

                st.markdown(
                    f"""
                    <div class="candidate-card">

                        <div style="
                            display:flex;
                            align-items:center;
                            gap:15px;
                        ">

                            <div style="
                                width:55px;
                                height:55px;
                                border-radius:50%;
                                background:#e6f0ff;
                                color:#2457a6;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-size:18px;
                                font-weight:800;
                            ">
                                {initials}
                            </div>

                            <div>

                                <div class="candidate-name">
                                    {clean_name}
                                </div>

                                <div class="candidate-meta">
                                    Rank #{rank}
                                    &nbsp; • &nbsp;
                                    {result["matched_role"]}
                                    &nbsp; • &nbsp;
                                    {result["career_stage"]}
                                </div>

                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # SCORE
                # --------------------------------------------

                st.markdown(
                    f"""
                    <div style="margin-top:20px;">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                        ">

                            <span style="
                                color:#425875;
                                font-size:13px;
                                font-weight:700;
                            ">
                                Overall Match
                            </span>

                            <span class="score-number">
                                {score}%
                            </span>

                        </div>

                        <div class="score-bar-background">

                            <div
                                class="score-bar-fill"
                                style="
                                    width:{min(score, 100)}%;
                                ">
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # SCORE BREAKDOWN
                # --------------------------------------------

                st.markdown(
                    "### Match Breakdown"
                )

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.metric(
                        "Skill Match",
                        f'{result["skill_score"]}%'
                    )

                with c2:

                    st.metric(
                        "Experience",
                        f'{result["experience_score"]}%'
                    )

                with c3:

                    st.metric(
                        "Projects",
                        f'{result["project_score"]}%'
                    )

                with c4:

                    st.metric(
                        "Education",
                        f'{result["education_score"]}%'
                    )


                # --------------------------------------------
                # STRENGTHS / MISSING
                # --------------------------------------------

                left, right = st.columns(
                    2,
                    gap="medium"
                )

                with left:

                    st.markdown(
                        "### Candidate Strengths"
                    )

                    for strength in result["strengths"]:

                        st.markdown(
                            f"✓ {strength}"
                        )


                with right:

                    st.markdown(
                        "### Missing Skills"
                    )

                    if result["missing_skills"]:

                        html = ""

                        for skill in result["missing_skills"]:

                            html += (
                                '<span class="skill-chip '
                                'missing-chip">'
                                f'✕ {skill}'
                                '</span>'
                            )

                        st.markdown(
                            html,
                            unsafe_allow_html=True
                        )

                    else:

                        st.success(
                            "No major skill gaps identified."
                        )


                # --------------------------------------------
                # MATCHED SKILLS
                # --------------------------------------------

                st.markdown(
                    "### Matched Skills"
                )

                if result["matched_skills"]:

                    html = ""

                    for skill in result["matched_skills"]:

                        html += (
                            '<span class="skill-chip '
                            'matched-chip">'
                            f'✓ {skill}'
                            '</span>'
                        )

                    st.markdown(
                        html,
                        unsafe_allow_html=True
                    )

                else:

                    st.info(
                        "No required skills were matched."
                    )


                # --------------------------------------------
                # ROLE MATCHING
                # --------------------------------------------

                st.markdown(
                    "### Role Matching"
                )

                role1, role2 = st.columns(2)

                with role1:

                    st.metric(
                        "Requested Role",
                        result["requested_role"]
                    )

                with role2:

                    st.metric(
                        "Semantic Role Similarity",
                        f'{result["role_similarity"]}%'
                    )


    # ========================================================
    # CANDIDATE COMPARISON
    # ========================================================

    if valid_results:

        st.markdown(
            '<div class="section-title">Candidate Comparison</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-subtitle">
                Compare multiple candidates side by side.
            </div>
            """,
            unsafe_allow_html=True
        )

        candidate_names = [
            result["candidate"]
            for result in valid_results
        ]

        selected_candidates = st.multiselect(
            "Select candidates",
            candidate_names,
            default=(
                candidate_names[:2]
                if len(candidate_names) >= 2
                else candidate_names
            )
        )

        if selected_candidates:

            comparison_data = []

            for result in valid_results:

                if result["candidate"] not in selected_candidates:
                    continue

                comparison_data.append(
                    {
                        "Candidate":
                            result["candidate"],

                        "Overall":
                            f'{result["overall_score"]}%',

                        "Skills":
                            f'{result["skill_score"]}%',

                        "Experience":
                            f'{result["experience_score"]}%',

                        "Projects":
                            f'{result["project_score"]}%',

                        "Education":
                            f'{result["education_score"]}%',

                        "Career Stage":
                            result["career_stage"]
                    }
                )

            comparison_df = pd.DataFrame(
                comparison_data
            )

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )


    # ========================================================
    # FAILED FILES
    # ========================================================

    if failed_results:

        st.warning(
            f"{len(failed_results)} resume(s) "
            "could not be processed."
        )

        for result in failed_results:

            st.error(
                f'{result["candidate"]}: '
                f'{result["error"]}'
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Resume Screening System
        &nbsp; • &nbsp;
        MiniLM Semantic Matching
        &nbsp; • &nbsp;
        DistilBERT Resume-NER
        &nbsp; • &nbsp;
        Hybrid Candidate Ranking
    </div>
    """,
    unsafe_allow_html=True
)