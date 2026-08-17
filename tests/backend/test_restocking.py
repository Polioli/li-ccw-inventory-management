"""
Tests for the budget-based restocking recommendation endpoint.
"""
import pytest


class TestRestockingEndpoints:
    """Test suite for restocking recommendation endpoint."""

    def test_get_recommendations_success(self, client):
        """Test that a valid budget returns 200 with all required fields."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        assert response.status_code == 200

        data = response.json()
        required_fields = [
            "budget",
            "total_cost",
            "remaining_budget",
            "budget_utilized_percent",
            "items_needing_restock",
            "items_recommended",
            "recommendations",
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        assert isinstance(data["recommendations"], list)

    def test_recommendation_item_fields(self, client):
        """Test that each recommendation item has the expected fields."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        data = response.json()

        assert len(data["recommendations"]) > 0, "Expected at least one recommendation for budget=5000"

        item_fields = [
            "sku", "name", "category", "warehouse", "quantity_on_hand",
            "reorder_point", "target_stock_level", "quantity_needed",
            "quantity_to_order", "unit_cost", "line_total", "trend",
            "priority", "priority_reason", "fully_funded",
        ]
        for item in data["recommendations"]:
            for field in item_fields:
                assert field in item, f"Missing field: {field}"

    def test_budget_math_is_consistent(self, client):
        """Test that total_cost + remaining_budget == budget, and total_cost never exceeds budget."""
        for budget in [1, 50, 500, 5000, 50000]:
            response = client.get(f"/api/restocking/recommendations?budget={budget}")
            data = response.json()

            assert data["total_cost"] <= data["budget"]
            assert abs((data["total_cost"] + data["remaining_budget"]) - data["budget"]) < 0.01

    def test_quantity_to_order_never_exceeds_needed(self, client):
        """Test that quantity_to_order is always <= quantity_needed, and line_total matches."""
        response = client.get("/api/restocking/recommendations?budget=5000")
        data = response.json()

        for item in data["recommendations"]:
            assert item["quantity_to_order"] <= item["quantity_needed"]
            expected_line_total = round(item["quantity_to_order"] * item["unit_cost"], 2)
            assert abs(item["line_total"] - expected_line_total) < 0.01

            if item["quantity_to_order"] < item["quantity_needed"]:
                assert item["fully_funded"] is False
            else:
                assert item["fully_funded"] is True

    def test_recommendations_sorted_by_priority(self, client):
        """Test that high priority items never appear after lower priority items."""
        response = client.get("/api/restocking/recommendations?budget=1000000")
        data = response.json()

        priority_rank = {"high": 0, "medium": 1, "low": 2}
        ranks = [priority_rank[item["priority"]] for item in data["recommendations"]]

        assert ranks == sorted(ranks), "Recommendations should be sorted by priority (high, medium, low)"

    def test_negative_budget_returns_400(self, client):
        """Test that a negative budget is rejected."""
        response = client.get("/api/restocking/recommendations?budget=-10")
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_zero_budget_returns_400(self, client):
        """Test that a zero budget is rejected."""
        response = client.get("/api/restocking/recommendations?budget=0")
        assert response.status_code == 400

    def test_missing_budget_returns_422(self, client):
        """Test that a missing budget query param is rejected by FastAPI validation."""
        response = client.get("/api/restocking/recommendations")
        assert response.status_code == 422

    def test_huge_budget_funds_every_candidate(self, client):
        """Test that a very large budget fully funds every candidate item."""
        response = client.get("/api/restocking/recommendations?budget=100000000")
        data = response.json()

        assert data["items_recommended"] == data["items_needing_restock"]
        assert all(item["fully_funded"] for item in data["recommendations"])

    def test_tiny_budget_funds_few_items(self, client):
        """Test that a very small budget funds at most a couple of cheap items."""
        response = client.get("/api/restocking/recommendations?budget=1")
        data = response.json()

        assert len(data["recommendations"]) <= 1
        assert data["remaining_budget"] >= 0

    def test_warehouse_filter_narrows_candidates(self, client):
        """Test that filtering by warehouse only considers items in that warehouse."""
        response = client.get("/api/restocking/recommendations?budget=1000000&warehouse=Tokyo")
        assert response.status_code == 200

        data = response.json()
        for item in data["recommendations"]:
            assert item["warehouse"] == "Tokyo"

    def test_category_filter_narrows_candidates(self, client):
        """Test that filtering by category only considers items in that category."""
        response = client.get("/api/restocking/recommendations?budget=1000000&category=Sensors")
        assert response.status_code == 200

        data = response.json()
        for item in data["recommendations"]:
            assert item["category"] == "Sensors"

    def test_all_filter_values_match_no_filter(self, client):
        """Test that 'all' filter values behave the same as no filters."""
        response = client.get("/api/restocking/recommendations?budget=1000000&warehouse=all&category=all")
        response_no_filter = client.get("/api/restocking/recommendations?budget=1000000")

        assert response.json() == response_no_filter.json()
