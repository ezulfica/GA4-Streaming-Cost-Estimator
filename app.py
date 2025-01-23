import streamlit as st
from src.func import initialize_app, display_hypothesis, get_user_inputs, calculate_costs, display_results


def main():
    provider = initialize_app()
    params = display_hypothesis(provider)
    num_events, start_date, retention = get_user_inputs()
    df = calculate_costs(num_events, start_date, retention, params)
    display_results(df, retention)


if __name__ == "__main__":
    main()
