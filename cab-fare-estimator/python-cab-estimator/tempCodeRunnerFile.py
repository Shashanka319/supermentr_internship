port sections to interact with the system.
        """)

# Main Application Flow
if not st.session_state.authenticated:
    # Show authentication forms
    if st.session_state.show_signup:
        show_signup_form()
    else:
        show_login_form()
else:
    # Show authenticated user interface
    show_authenticated_app()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    🚕 <strong>Cab Fare Estimator</strong> - Reliable Transportation Solutions<br>
    Making your journey affordable and transparent
</div>
""", unsafe_allow_html=True)