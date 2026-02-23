from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PublicFeedback, UserRole, User

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/v1/feedback')

@feedback_bp.route('/', methods=['POST'])
def submit_feedback():
    """Submit public feedback for a shop"""
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        required_fields = ['shop_code', 'rating', 'comments']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
            
        # Create new feedback record
        feedback = PublicFeedback(
            shop_code=data['shop_code'],
            rating=rating,
            comments=data['comments'],
            customer_contact=data.get('customer_contact', None)
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit feedback: {str(e)}'}), 500

@feedback_bp.route('/', methods=['GET'])
@jwt_required()
def get_feedbacks():
    """Retrieve feedback (Requires Admin or Shop Manager role)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Parse query parameters
        shop_code = request.args.get('shop_code')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = PublicFeedback.query
        
        # Apply role-based filtering
        if user.role == UserRole.SHOP_MANAGER.value:
            if not user.shop_id:
                return jsonify({'error': 'Shop Manager is not assigned to a shop'}), 403
            
            # Shop manager can only see feedback for their own shop code
            # We need to query the shop to get its code
            from models import Shop
            shop = Shop.query.get(user.shop_id)
            if not shop:
                return jsonify({'error': 'Assigned shop not found'}), 404
                
            query = query.filter_by(shop_code=shop.shop_code)
        elif user.role != UserRole.ADMIN.value and user.role != UserRole.ANALYST.value:
             return jsonify({'error': 'Permission denied'}), 403
            
        # Apply explicit filters if provided (and user is admin or analyst)
        if shop_code and user.role in [UserRole.ADMIN.value, UserRole.ANALYST.value]:
            query = query.filter_by(shop_code=shop_code)
            
        # Execute query with pagination and ordering
        total = query.count()
        feedbacks = query.order_by(PublicFeedback.created_at.desc()) \
                        .limit(limit) \
                        .offset(offset) \
                        .all()
                        
        return jsonify({
            'feedbacks': [{
                'id': f.id,
                'shop_code': f.shop_code,
                'rating': f.rating,
                'comments': f.comments,
                'customer_contact': f.customer_contact,
                'status': f.status,
                'created_at': f.created_at.isoformat()
            } for f in feedbacks],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve feedbacks: {str(e)}'}), 500
