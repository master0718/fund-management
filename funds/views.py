import csv
import io
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
from .models import Fund
from .forms import CSVUploadForm

def fund_list(request):
    strategy_filter = request.GET.get('strategy', '')
    
    if strategy_filter:
        funds = Fund.objects.filter(strategy=strategy_filter)
    else:
        funds = Fund.objects.all()
    
    # Get summary statistics
    total_count = funds.count()
    total_aum = funds.aggregate(total=Sum('aum'))['total'] or Decimal('0')
    
    # Get available strategies for dropdown
    strategies = Fund.objects.values_list('strategy', flat=True).distinct()
    
    context = {
        'funds': funds,
        'strategies': strategies,
        'selected_strategy': strategy_filter,
        'total_count': total_count,
        'total_aum': total_aum,
    }
    return render(request, 'funds/fund_list.html', context)

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read and parse CSV
            decoded_file = csv_file.read().decode('utf-8-sig')  # Use utf-8-sig to handle BOM
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            # Get the actual column names from the CSV
            fieldnames = csv_data.fieldnames
            print(f"CSV columns found: {fieldnames}")  # Debug info
            
            funds_created = 0
            for row in csv_data:
                print(f"Processing row: {row}")  # Debug info
                
                # Handle different possible column name variations (including BOM)
                name = row.get('Name') or row.get('\ufeffName') or row.get('name') or row.get('NAME')
                strategy = row.get('Strategy') or row.get('strategy') or row.get('STRATEGY')
                aum_raw = row.get('AUM (USD)') or row.get('aum') or row.get('AUM')
                inception_raw = row.get('Inception Date') or row.get('inception_date') or row.get('Inception')
                
                # Validate required fields
                if not name or not strategy:
                    print(f"Skipping row - missing name or strategy: {row}")
                    continue
                
                # Parse AUM (handle empty values)
                aum = None
                if aum_raw and str(aum_raw).strip():
                    try:
                        aum = Decimal(str(aum_raw).replace(',', ''))
                    except (ValueError, TypeError):
                        print(f"Could not parse AUM value: {aum_raw}")
                        pass
                
                # Parse inception date
                inception_date = None
                if inception_raw and str(inception_raw).strip():
                    try:
                        # Try different date formats
                        date_str = str(inception_raw).strip()
                        for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d', '%d/%m/%Y']:
                            try:
                                inception_date = datetime.strptime(date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        if not inception_date:
                            print(f"Could not parse date: {inception_raw}")
                    except Exception as e:
                        print(f"Date parsing error: {e}")
                        pass
                
                # Create Fund object
                try:
                    Fund.objects.create(
                        name=name.strip(),
                        strategy=strategy.strip(),
                        aum=aum,
                        inception_date=inception_date
                    )
                    funds_created += 1
                    print(f"Created fund: {name}")
                except Exception as e:
                    print(f"Error creating fund {name}: {e}")
            
            return render(request, 'funds/upload.html', {
                'form': CSVUploadForm(),
                'success_message': f'Successfully imported {funds_created} funds!'
            })
    else:
        form = CSVUploadForm()
    
    return render(request, 'funds/upload.html', {'form': form})

# API Views
@csrf_exempt
def api_fund_list(request):
    strategy_filter = request.GET.get('strategy', '')
    
    if strategy_filter:
        funds = Fund.objects.filter(strategy=strategy_filter)
    else:
        funds = Fund.objects.all()
    
    fund_data = []
    for fund in funds:
        fund_data.append({
            'id': fund.id,
            'name': fund.name,
            'strategy': fund.strategy,
            'aum': float(fund.aum) if fund.aum else None,
            'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
        })
    
    return JsonResponse({'funds': fund_data})

@csrf_exempt
def api_fund_detail(request, fund_id):
    fund = get_object_or_404(Fund, id=fund_id)
    fund_data = {
        'id': fund.id,
        'name': fund.name,
        'strategy': fund.strategy,
        'aum': float(fund.aum) if fund.aum else None,
        'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
    }
    return JsonResponse(fund_data)
